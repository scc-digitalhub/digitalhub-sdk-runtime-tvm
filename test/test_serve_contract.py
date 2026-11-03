# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

import pytest
from pydantic import ValidationError

from digitalhub_runtime_tvm.entities.model.tvm.models import TensorSpec
from digitalhub_runtime_tvm.entities.run.serve.spec import RunSpecTvmRunServe, RunValidatorTvmRunServe


def test_serve_spec_round_trip():
    options = {
        "task": "tvm+serve://test/task",
        "model_path": "store://test/model/tvm-so/model:version",
        "served_name": "model-1",
        "image": "example/runtime:test",
        "replicas": 0,
        "workers": 2,
        "service_type": "ClusterIP",
        "service_name": "public",
    }
    spec = RunSpecTvmRunServe(**options).to_dict()
    validated = RunValidatorTvmRunServe.model_validate(spec).model_dump(mode="json", exclude_none=True)
    assert validated == {**options, "inputs": {}}
    assert RunSpecTvmRunServe(**validated).to_dict() == spec


def test_serve_spec_does_not_invent_runtime_defaults():
    spec = RunSpecTvmRunServe(task="tvm+serve://test/task").to_dict()
    assert spec == {"task": "tvm+serve://test/task", "inputs": {}}
    assert RunValidatorTvmRunServe.model_validate(spec).model_dump(mode="json", exclude_none=True) == spec


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("model_path", "/tmp/model"),
        ("model_path", "store://test/artifact/tvm-so/model:version"),
        ("served_name", "model/name"),
        ("served_name", "-model"),
        ("served_name", ""),
        ("replicas", -1),
        ("workers", 0),
        ("service_type", "Unsupported"),
    ],
)
def test_invalid_serve_options_are_rejected(field, value):
    with pytest.raises(ValidationError) as error:
        RunValidatorTvmRunServe.model_validate({"task": "tvm+serve://test/task", field: value})
    assert error.value.errors()[0]["loc"] == (field,)


@pytest.mark.parametrize("shape", [[], [-1, 3], [1, 4]])
def test_tensor_signature_serialization_preserves_shape_and_quantization(shape):
    values = {
        "name": "x",
        "dtype": "int8",
        "shape": shape,
        "scale": [0.125],
        "zero_point": [-3],
        "quantized_dimension": 1,
    }
    spec = TensorSpec.model_validate(values)
    assert spec.to_dict() == values
    assert TensorSpec.model_validate_json(spec.model_dump_json()) == spec
