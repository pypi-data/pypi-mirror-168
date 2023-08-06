use std::path::Path;
use tract_hir::prelude::*;

use anyhow::{bail, Context, Result};
use ffi_convert::{CReprOf, RawBorrow, RawPointerConverter};
use std::cell::RefCell;
use std::ffi::CString;

mod loader;
mod npz;

use loader::load_model;
use npz::{for_npz, npz_add_tensor};

thread_local! {
    pub(crate) static LAST_ERROR: RefCell<Option<String>> = RefCell::new(None);
}
/// Used as a return type of functions that can encounter errors.
/// If the function encountered an error, you can retrieve it using the `tract_get_last_error`
/// function.
#[repr(C)]
#[allow(non_camel_case_types)]
#[derive(Debug, PartialEq, Eq)]
pub enum TractResult {
    /// The function returned successfully
    TRACT_OK = 0,
    /// The function returned an error
    TRACT_KO = 1,
}

#[repr(C)]
#[derive(Debug)]
pub struct CTypedModelPlan(*mut libc::c_void);

fn wrap<F: FnOnce() -> anyhow::Result<()>>(func: F) -> TractResult {
    match func() {
        Ok(_) => TractResult::TRACT_OK,
        Err(e) => {
            let msg = format!("{:#?}", e);
            if std::env::var("TRACT_ERROR_STDERR").is_ok() {
                eprintln!("{}", msg);
            }
            LAST_ERROR.with(|p| *p.borrow_mut() = Some(msg));
            TractResult::TRACT_KO
        }
    }
}

#[no_mangle]
pub extern "C" fn tract_get_last_error(error: *mut *mut ::libc::c_char) -> TractResult {
    wrap(move || {
        LAST_ERROR.with(|msg| {
            let string = msg
                .borrow_mut()
                .take()
                .unwrap_or_else(|| "No error message".to_string());
            let result: *const ::libc::c_char =
                std::ffi::CString::c_repr_of(string)?.into_raw_pointer();
            unsafe { *error = result as _ }
            Ok(())
        })
    })
}

#[no_mangle]
pub extern "C" fn tract_destroy_buffer(ptr: *mut libc::c_char) -> TractResult {
    unsafe { libc::free(ptr as *mut libc::c_void) }
    TractResult::TRACT_OK
}

#[no_mangle]
pub extern "C" fn tract_destroy_plan(plan_ptr: *mut *const CTypedModelPlan) -> TractResult {
    wrap(|| unsafe {
        TypedRunnableModel::<TypedModel>::drop_raw_pointer(
            CTypedModelPlan::raw_borrow(*plan_ptr)?.0 as *mut TypedRunnableModel<TypedModel>,
        )?;
        Ok(())
    })
}

#[no_mangle]
pub extern "C" fn tract_destroy_string(ptr: *mut libc::c_char) -> TractResult {
    {
        unsafe { CString::from_raw(ptr) };
    }
    TractResult::TRACT_OK
}

macro_rules! create_rust_str_from {
    ($pointer:expr) => {{
        unsafe { ::std::ffi::CStr::raw_borrow($pointer) }?
            .to_str()
            .context("Could not convert pointer to rust str")?
    }};
}
macro_rules! get_typed_model_plan_from {
    ($pointer:expr) => {{
        unsafe {
            TypedRunnableModel::<TypedModel>::raw_borrow(
                CTypedModelPlan::raw_borrow($pointer)?.0 as *mut TypedRunnableModel<TypedModel>,
            )?
        }
    }};
}

/// load simple tract Plan of TypedModel from various serialization:
/// NNEF: folder or tgz
/// ONNX
pub fn call_load_plan_from_path(
    path_string: *const libc::c_char,
    plan_ptr: *mut *const CTypedModelPlan,
) -> Result<()> {
    let path = Path::new(create_rust_str_from!(path_string));
    let typed_model = load_model(path)?;
    let plan: TypedRunnableModel<TypedModel> =
        SimplePlan::new(typed_model.into_decluttered()?.into_optimized()?)?;

    let cplan = CTypedModelPlan(plan.into_raw_pointer() as _);
    unsafe { *plan_ptr = cplan.into_raw_pointer() as _ };

    Ok(())
}

pub fn call_run_typed_model_plan(
    plan_ptr: *mut *const CTypedModelPlan,
    npz_inputs_buffer_ptr: *const libc::c_char,
    npz_input_buffer_length: libc::size_t,
    npz_outputs_buffer_ptr: *mut *mut ::libc::c_char,
    npz_outputs_buffer_length: *mut libc::size_t,
) -> Result<()> {
    let plan = get_typed_model_plan_from!(*plan_ptr);

    // load npz into ndarray
    let bits: &[u8] = unsafe {
        ::std::slice::from_raw_parts_mut(
            npz_inputs_buffer_ptr as *mut u8,
            npz_input_buffer_length as usize,
        )
    };
    let raw = std::io::Cursor::new(bits);
    let mut input_npz = ndarray_npy::NpzReader::new(raw)?;
    let vectors = input_npz
        .names()?
        .iter()
        .map(|n| {
            let name = n.trim_end_matches(".npy").to_string();
            let node_id = plan.model.node_by_name(name)?.id;
            Ok((node_id, for_npz(&mut input_npz, &n)?))
        })
        .collect::<Result<Vec<(usize, Tensor)>>>()?;

    // ensure model inputs order
    let ordered_vectors = plan
        .model
        .inputs
        .iter()
        .map(|outlet_uid| {
            let possible_match = vectors
                .iter()
                .find(|(node_id, _)| node_id == &outlet_uid.node);

            match possible_match {
                Some((_, tensor)) => Ok(tensor.to_owned()),
                _ => bail!(
                    "input with id: {:#?} not provided",
                    plan.model.node(outlet_uid.node).name
                ),
            }
        })
        .collect::<Result<Vec<_>>>()?;

    let svec = TVec::from_vec(ordered_vectors);
    // run network with npz content
    let results = plan
        .clone()
        .run(svec)?
        .iter()
        .map(|t| t.to_owned().into_arc_tensor())
        .collect::<Vec<Arc<Tensor>>>();

    // write output npz from ndarray
    let mut output_buffer = Vec::<u8>::new();
    {
        // closure to limit borrow buffer using cursor
        let mut output_npz = ndarray_npy::NpzWriter::new(std::io::Cursor::new(&mut output_buffer));
        for (ix, output) in results.iter().enumerate() {
            let name = plan
                .model
                .outlet_label(plan.model.output_outlets()?[ix])
                .map(|name| name.to_string())
                .unwrap_or_else(|| format!("output_{}", ix));
            npz_add_tensor(&mut output_npz, name, output)?;
        }
    }
    let outputs_buffer_len = output_buffer.len();
    unsafe {
        let c_buffer = std::ffi::CString::from_vec_unchecked(output_buffer);
        let result_raw_ptr: *const ::libc::c_char = c_buffer.into_raw_pointer();
        *npz_outputs_buffer_ptr = result_raw_ptr as _;
        *npz_outputs_buffer_length = outputs_buffer_len as _;
    }

    Ok(())
}

#[no_mangle]
pub unsafe extern "C" fn load_plan_from_path(
    path_string: *const libc::c_char,
    plan_ptr: *mut *const CTypedModelPlan,
) -> TractResult {
    wrap(|| call_load_plan_from_path(path_string, plan_ptr))
}

#[no_mangle]
pub unsafe extern "C" fn run_typed_model_plan(
    plan_ptr: *mut *const CTypedModelPlan,
    npz_inputs_buffer_ptr: *const libc::c_char,
    npz_input_buffer_length: libc::size_t,
    npz_outputs_buffer_ptr: *mut *mut ::libc::c_char,
    npz_outputs_buffer_length: *mut libc::size_t,
) -> TractResult {
    wrap(|| {
        call_run_typed_model_plan(
            plan_ptr,
            npz_inputs_buffer_ptr,
            npz_input_buffer_length,
            npz_outputs_buffer_ptr,
            npz_outputs_buffer_length,
        )
    })
}
