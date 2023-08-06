///
/// This module is a simplified version of tract/cli/src/params.rs
///
use anyhow::{bail, format_err, Result};
use std::path::Path;
use tract_hir::prelude::*;
use tract_pulse::WithPulse;

fn guess_format_from_filepath(path: &Path) -> &str {
    if path.extension().map(|s| s == "onnx").unwrap_or(false) {
        "onnx"
    } else if path
        .extension()
        .map(|s| s == "raw" || s == "txt")
        .unwrap_or(false)
    {
        "kaldi"
    } else if path.is_dir()
        || path.to_string_lossy().ends_with(".tar")
        || path.to_string_lossy().ends_with(".tar.gz")
        || path.extension().map(|s| s == "tgz").unwrap_or(false)
    {
        "nnef"
    } else {
        "tf"
    }
}

pub fn load_model(path: &Path) -> Result<TypedModel> {
    let format = guess_format_from_filepath(path);
    let model = match format {
        "nnef" => {
            let nnef = tract_nnef::nnef().with_tract_core().with_pulse();
            nnef
            .model_for_path(path)
            .map_err(|e| format_err!("Load NNEF model: {:?}", e))?
        }
        "onnx" => {
            let onnx = tract_onnx::onnx();
            let model = onnx.model_for_path(path)
                .map_err(|e| format_err!("Load ONNX model: {:?}", e))?;
            model.into_typed()?
        }
        _ => bail!(
            "Format {} not supported by tract_python. You may need to add a Pull Request with the right features.",
            format
        ),
    };
    Ok(model)
}
