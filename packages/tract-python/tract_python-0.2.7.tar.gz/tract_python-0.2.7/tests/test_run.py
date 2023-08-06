from pathlib import Path
import tract_python
import numpy as np
from urllib import request
from tract_python import TractRuntimeError, TractTypeError, TractModelInitError

test_dir = Path(__file__).parent
assets_dir = test_dir / "assets"


def simple_model_load_and_execute_n_times(mul_model_path):
    tm = tract_python.TractModel.load_from_path(mul_model_path)

    init_input = np.arange(6).reshape(1, 2, 3).astype(np.float32)
    expected_output = np.arange(6).reshape(1, 2, 3).astype(np.float32) * 2
    results = tm.run(input_0=init_input)
    assert np.allclose(
        results["output_0"],
        expected_output,
    )

    results2 = tm.run(input_0=init_input * 2)
    assert np.allclose(
        results2["output_0"],
        expected_output * 2,
    )


def test_mul2_nnef():
    simple_model_load_and_execute_n_times(assets_dir / "mul2.nnef.tgz")


def test_mul2_onnx():
    return simple_model_load_and_execute_n_times(assets_dir / "mul.onnx")


def test_load_onnx_tract_unable():
    local_model_path = assets_dir / "resnet50.onnx"
    request.urlretrieve(
        "https://huggingface.co/OWG/resnet-50/raw/main/onnx/model.onnx",
        local_model_path,
    )
    try:
        tract_python.TractModel.load_from_path(local_model_path)
    except TractRuntimeError as exp:
        # expect fail at load time since tract error
        assert "invalid wire type value: 6" in exp.args[0]


def test_wrong_inputs_name():
    tm = tract_python.TractModel.load_from_path(assets_dir / "mul2.nnef.tgz")
    init_input = np.arange(6).reshape(1, 2, 3).astype(np.float32)
    try:
        tm.run(my_wrong_input_name=init_input)
    except TractRuntimeError as exp:
        assert (
            'No node found for name: "my_wrong_input_name"' in exp.args[0]
        ), exp.args[0]


def test_missing_input():
    tm = tract_python.TractModel.load_from_path(assets_dir / "mul2.nnef.tgz")
    try:
        tm.run()
    except TractRuntimeError as exp:
        assert (
            'input with id: \\"input_0\\" not provided' in exp.args[0]
        ), exp.args[0]


def test_wrong_input_type():
    tm = tract_python.TractModel.load_from_path(assets_dir / "mul2.nnef.tgz")
    init_input = np.arange(6).reshape(1, 2, 3).astype(np.int64)
    try:
        tm.run(input_0=init_input)
    except TractRuntimeError as exp:
        assert all(
            _ in exp.args[0]
            for _ in ("Error while running plan", "Evaluating", "F32", "I64")
        ), exp.args[0]


def test_wrong_run_parameters():
    tm = tract_python.TractModel.load_from_path(assets_dir / "mul2.nnef.tgz")
    try:
        tm.run(**{"input_0": None})
    except TractTypeError as exp:
        assert "have np.ndarray as values" in exp.args[0]


def test_wrong_init_model():
    try:
        tract_python.TractModel(None, assets_dir / "not_exists.nnef.tgz")
    except TractModelInitError as exp:
        assert "does not exists" in exp.args[0]
