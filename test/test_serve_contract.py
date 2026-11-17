# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

import json
import os
from pathlib import Path
from unittest import mock

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from digitalhub_runtime_tvm.entities.function.tvm.spec import FunctionSpecTvm
from digitalhub_runtime_tvm.entities.function.tvm.crud import new_function_tvm
from digitalhub_runtime_tvm.entities.model.tvm.models import TensorSpec
from digitalhub_runtime_tvm.entities.run.serve.spec import RunSpecTvmRunServe
from digitalhub_runtime_tvm.entities.task.serve.spec import TaskSpecTvmServe


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
    validated = RunSpecTvmRunServe.model_validate(spec).model_dump(mode="json", exclude_none=True)
    assert validated == {**options, "inputs": {}}
    assert RunSpecTvmRunServe(**validated).to_dict() == spec


def test_serve_spec_does_not_invent_runtime_defaults():
    spec = RunSpecTvmRunServe(
        task="tvm+serve://test/task", model_path="store://test/model/tvm-so/model:version"
    ).to_dict()
    assert spec == {
        "task": "tvm+serve://test/task",
        "model_path": "store://test/model/tvm-so/model:version",
        "inputs": {},
    }
    assert RunSpecTvmRunServe.model_validate(spec).model_dump(mode="json", exclude_none=True) == spec


@pytest.mark.parametrize(
    "model_path", [None, "", " ", "store://test/model/tvm-so/model", "store://test/model/tvm-ir/model:version"]
)
def test_serve_requires_a_versioned_compiled_model(model_path):
    with pytest.raises(ValidationError):
        RunSpecTvmRunServe(task="tvm+serve://test/task", model_path=model_path)


def test_serve_cannot_use_a_legacy_function_or_run_reference():
    with pytest.raises(ValidationError):
        RunSpecTvmRunServe(task="tvm+serve://test/task", so_model="store://test/model/tvm-so/model:old")
    assert "so_model" not in FunctionSpecTvm.model_fields
    assert "so_model" not in RunSpecTvmRunServe.model_fields
    assert TaskSpecTvmServe(function="tvm://test/model:version").model_path is None


def test_legacy_function_and_run_snapshots_remain_readable_without_mutation():
    source = {"model": "store://test/model/onnx/model:v1", "so_model": "store://test/model/tvm-so/model:old"}
    function = FunctionSpecTvm.model_validate(source)
    assert "so_model" not in function.to_dict()
    assert source["so_model"] == "store://test/model/tvm-so/model:old"
    run = {
        "task": "tvm+serve://test/task",
        "model_path": "store://test/model/tvm-so/model:chosen",
        "so_model": source["so_model"],
    }
    parsed = RunSpecTvmRunServe.model_validate(run).to_dict()
    assert parsed["model_path"] == "store://test/model/tvm-so/model:chosen"
    assert "so_model" not in parsed
    assert "so_model" in run


def test_legacy_crud_positional_arguments_keep_uuid_and_version():
    with mock.patch("digitalhub_runtime_tvm.entities.function.tvm.crud.new_function") as create:
        new_function_tvm("project", "model", "source.onnx", "onnx", "ir-key", "legacy-so", "uuid", "version")
    assert create.call_args.kwargs["uuid"] == "uuid"
    assert create.call_args.kwargs["version"] == "version"
    assert "so_model" not in create.call_args.kwargs


def test_legacy_crud_keyword_does_not_store_a_compiled_model():
    with mock.patch("digitalhub_runtime_tvm.entities.function.tvm.crud.new_function") as create:
        new_function_tvm("project", "model", "source.onnx", so_model="legacy-so", uuid="uuid")
    assert create.call_args.kwargs["uuid"] == "uuid"
    assert "so_model" not in create.call_args.kwargs


@pytest.mark.parametrize(
    "model_path",
    [
        "store://test/model/tvm-so/model:arm64",
        "store://test/model/tvm-so/model:amd64",
        None,
        "",
        " ",
        "store://test/model/tvm-so/model",
        "store://test/model/tvm-ir/model:version",
    ],
)
def test_model_selection_matches_the_core_export(model_path):
    schema_dir = os.environ.get("TVM_CORE_SCHEMA_DIR")
    if not schema_dir:
        pytest.skip("CORE schema export directory not supplied")
    schema = json.loads((Path(schema_dir) / "run" / "tvm+serve:run.json").read_text())
    data = {"task": "tvm+serve://test/task", "function": "tvm://test/model:v1", "model_path": model_path}
    core_accepts = Draft202012Validator(schema).is_valid(data)
    try:
        RunSpecTvmRunServe.model_validate(data)
    except ValidationError:
        assert not core_accepts
    else:
        assert core_accepts


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
        RunSpecTvmRunServe.model_validate(
            {"task": "tvm+serve://test/task", "model_path": "store://test/model/tvm-so/model:version", field: value}
        )
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
