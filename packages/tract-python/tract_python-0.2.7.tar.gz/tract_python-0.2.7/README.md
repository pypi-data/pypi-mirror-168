# tract-python

 [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
 [![PyPI version](https://badge.fury.io/py/tract_python.svg)](https://badge.fury.io/py/tract_python)
 [![CI](https://github.com/DreamerMind/tract-python/actions/workflows/CI.yml/badge.svg?branch=main)](https://github.com/DreamerMind/tract-python/actions/workflows/CI.yml)

[tract inference engine](https://github.com/sonos/tract) bindings in Python via FFI.
It support Neural Network inference from NNEF or ONNX.

## Why

No need to compile tract or have cargo installed, fast install.

`tract-cli` is very feature-full but reloading a model each time you wish
to do an inference is computationaly costy and slow.

Think `onnxruntime` except it support NNEF, and it is based on tract.

## Install

Install using pip:
```
pip install tract_python
```


## Usage

```python
import tract_python

print(tract_python.TRACT_VERSION)
# "X.X.X"

tract_model = tract_python.TractModel.load_from_path(
  # This parameter can be an ONNX or NNEF filepath (in case of NNEF it can be a dir or a tgz)
  './tests/assets/test_simple_nnef/' # simple graph that mul input by 2
)
# .run take as argument names the name of input nodes in your neural network
results = tract_model.run(input_0=np.arange(6).reshape(1, 2, 3).astype(np.float32))
print(results)
#{'output_0': array([[[ 0.,  2.,  4.],
#       [ 6.,  8., 10.]]], dtype=float32)}

```

## Status

This project is maintained with latest tract version.

## Scope

Our personnal usecase is to be able to run +10M inferences with 'tract' engine.
So loading/running NNEF or ONNX is sufficient.

We would be happy to support some others `tract-cli` features:
- [ ] computing: number of FMA operations
- [ ] computing: profiling infos

(Thought it would be better to extract from `tract-cli` a `tract-profile` crate first in original repo to avoid code duplicate)
We do not have the bandwith to do more and welcome any contributor that would wish to add more features.
