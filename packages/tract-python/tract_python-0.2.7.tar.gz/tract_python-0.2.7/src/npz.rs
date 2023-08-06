use anyhow::{bail, format_err, Result};
use tract_hir::prelude::*;

///
/// Borrowed from tract-cli with adapted npz type signature
pub fn for_npz(
    npz: &mut ndarray_npy::NpzReader<std::io::Cursor<&[u8]>>,
    name: &str,
) -> Result<Tensor> {
    if let Ok(t) = npz.by_name::<tract_ndarray::OwnedRepr<f32>, tract_ndarray::IxDyn>(name) {
        return Ok(t.into_tensor());
    }
    if let Ok(t) = npz.by_name::<tract_ndarray::OwnedRepr<f64>, tract_ndarray::IxDyn>(name) {
        return Ok(t.into_tensor());
    }
    if let Ok(t) = npz.by_name::<tract_ndarray::OwnedRepr<i8>, tract_ndarray::IxDyn>(name) {
        return Ok(t.into_tensor());
    }
    if let Ok(t) = npz.by_name::<tract_ndarray::OwnedRepr<i16>, tract_ndarray::IxDyn>(name) {
        return Ok(t.into_tensor());
    }
    if let Ok(t) = npz.by_name::<tract_ndarray::OwnedRepr<i32>, tract_ndarray::IxDyn>(name) {
        return Ok(t.into_tensor());
    }
    if let Ok(t) = npz.by_name::<tract_ndarray::OwnedRepr<i64>, tract_ndarray::IxDyn>(name) {
        return Ok(t.into_tensor());
    }
    if let Ok(t) = npz.by_name::<tract_ndarray::OwnedRepr<u8>, tract_ndarray::IxDyn>(name) {
        return Ok(t.into_tensor());
    }
    if let Ok(t) = npz.by_name::<tract_ndarray::OwnedRepr<u16>, tract_ndarray::IxDyn>(name) {
        return Ok(t.into_tensor());
    }
    if let Ok(t) = npz.by_name::<tract_ndarray::OwnedRepr<u32>, tract_ndarray::IxDyn>(name) {
        return Ok(t.into_tensor());
    }
    if let Ok(t) = npz.by_name::<tract_ndarray::OwnedRepr<u64>, tract_ndarray::IxDyn>(name) {
        return Ok(t.into_tensor());
    }
    if let Ok(t) = npz.by_name::<tract_ndarray::OwnedRepr<bool>, tract_ndarray::IxDyn>(name) {
        return Ok(t.into_tensor());
    }
    Err(format_err!("Can not extract tensor from {}", name))
}

pub fn npz_add_tensor(
    npz: &mut ndarray_npy::NpzWriter<std::io::Cursor<&mut Vec<u8>>>,
    name: String,
    tensor: &Arc<Tensor>,
) -> Result<()> {
    match tensor.datum_type() {
        DatumType::F16 => npz.add_array(name, &tensor.cast_to::<f32>()?.to_array_view::<f32>()?)?,
        DatumType::Bool => npz.add_array(name, &tensor.to_array_view::<bool>()?)?,
        DatumType::U8 => npz.add_array(name, &tensor.to_array_view::<u8>()?)?,
        DatumType::U16 => npz.add_array(name, &tensor.to_array_view::<u16>()?)?,
        DatumType::U32 => npz.add_array(name, &tensor.to_array_view::<u32>()?)?,
        DatumType::U64 => npz.add_array(name, &tensor.to_array_view::<u64>()?)?,
        DatumType::I8 => npz.add_array(name, &tensor.to_array_view::<i8>()?)?,
        DatumType::I16 => npz.add_array(name, &tensor.to_array_view::<i16>()?)?,
        DatumType::I32 => npz.add_array(name, &tensor.to_array_view::<i32>()?)?,
        DatumType::I64 => npz.add_array(name, &tensor.to_array_view::<i64>()?)?,
        DatumType::F32 => npz.add_array(name, &tensor.to_array_view::<f32>()?)?,
        DatumType::F64 => npz.add_array(name, &tensor.to_array_view::<f64>()?)?,
        DatumType::QI8(_) => npz.add_array(name, &tensor.to_array_view::<i8>()?)?,
        DatumType::QU8(_) => npz.add_array(name, &tensor.to_array_view::<u8>()?)?,
        DatumType::QI32(_) => npz.add_array(name, &tensor.to_array_view::<i32>()?)?,
        _ => bail!(format_err!(
            "Not writing {}, {:?}, unsupported type",
            name,
            tensor
        )),
    };
    Ok(())
}
