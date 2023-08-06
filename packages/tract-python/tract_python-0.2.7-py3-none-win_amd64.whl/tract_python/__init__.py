import typing as T
import io
from pathlib import Path

import numpy as np

from .tract_python import ffi, lib

__version__ = "0.2.7"

TRACT_VERSION = "0.18.0"


class TractPythonError(Exception):
    pass


class TractModelInitError(ValueError, TractPythonError):
    pass


class TractTypeError(TypeError, TractPythonError):
    pass


class TractRuntimeError(RuntimeError, TractPythonError):
    pass


def _string_at(ptr):
    return ffi.string(ptr[0])


_WARN_INSTANTIATION_CTYPE_MSG = (
    "typed_model_plan_ptr must be a ctype('struct CTypedModelPlan * *'). "
    "Wrong instantiation is unexpected. "
    "Maybe you didn't use '.load_from_path' method ?"
)


class TractModel:
    """Load a tract model plan in memory and allow run inferences on it

    Real Tract model behind FFI is deallocated from memory
    when this class instance is garbage collected.

    """

    def __init__(self, typed_model_plan_ptr, original_path: Path):
        if not Path(original_path).exists():
            raise TractModelInitError(f"{original_path} does not exists")
        try:
            ctype = ffi.typeof(typed_model_plan_ptr)
            if ctype.cname != "struct CTypedModelPlan * *":
                raise TractModelInitError(_WARN_INSTANTIATION_CTYPE_MSG)
        except Exception as e:
            raise TractModelInitError(_WARN_INSTANTIATION_CTYPE_MSG) from e
        self._typed_model_plan_ptr = typed_model_plan_ptr
        self._original_path = original_path

    def __del__(self):
        if hasattr(self, "_typed_model_plan_ptr"):
            lib.tract_destroy_plan(self._typed_model_plan_ptr)

    @classmethod
    def load_from_path(cls, path: T.Union[Path, str]) -> "TractModel":
        """Load any an ONNX or NNEF model plan from a filepath.

        In case of NNEF it can be a dir or a tgz.
        """
        path = Path(path)
        assert path.exists(), f"provided path: {path} does not exist"
        _model = ffi.new("CTypedModelPlan * *")
        exit_code = lib.load_plan_from_path(str(path).encode("utf-8"), _model)
        if exit_code:
            lib_error = ffi.new("char * *")
            lib.tract_get_last_error(lib_error)
            lib_error = _string_at(lib_error).decode("utf-8")
            raise TractRuntimeError(f"Error while creating plan: {lib_error}")
        return cls(_model, path)

    def run(self, **kwargs):
        """run an inference of this instance 'plan' with provided parameters.


        Args:
            Each parameter name must be a 'label' of an input node in
                the provided ONNX or NNEF model graph.
            All tensors provided must be numpy arrays (be carefull with types).
            All inputs need to be filled.

        Returns:
            dict with keys being model graph outputs labels and values numpy
            array containing the result for this node
        """
        for k, v in kwargs.items():
            if not isinstance(v, np.ndarray):
                raise TractTypeError(
                    ".run(**kwargs) need kwargs to have np.ndarray as values"
                )
        # We use npz format as exchange format between numpy and ndarray
        # this avoid to redefine all bindings for all types both side
        # at cost of some minor serializations slowdown

        # contains inputs npz equivalent
        inputs_buffer = io.BytesIO()
        np.savez(inputs_buffer, **kwargs)
        inputs_buffer.seek(0)
        inputs_buffer_bits = inputs_buffer.read()

        raw_output_ref = ffi.new("char * *")
        npz_outputs_buffer_length_ref = ffi.new("size_t *")
        # Call
        exit_code = lib.run_typed_model_plan(
            self._typed_model_plan_ptr,
            inputs_buffer_bits,
            len(inputs_buffer_bits),
            raw_output_ref,
            npz_outputs_buffer_length_ref,
        )

        if exit_code:
            lib_error = ffi.new("char * *")
            lib.tract_get_last_error(lib_error)
            lib_error = _string_at(lib_error).decode("utf-8")
            raise TractRuntimeError(f"Error while running plan: {lib_error}")

        outputs_buffer_len = ffi.unpack(npz_outputs_buffer_length_ref, 1)[0]
        raw_output_bytes = ffi.unpack(raw_output_ref[0], outputs_buffer_len)
        lib.tract_destroy_buffer(raw_output_ref[0])

        # reload output.npz
        # raw_output_ref is incorrect for now
        outputs_buffer = io.BytesIO(raw_output_bytes)
        outputs_buffer.seek(0)
        results = np.load(outputs_buffer)
        return dict(results)

    def __repr__(self) -> str:
        klass = self.__class__.__name__
        return f"<{klass} path='{self._original_path}'>"


__all__ = ["TractModel"]
