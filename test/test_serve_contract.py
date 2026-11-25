# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

import json
import os
from pathlib import Path
from unittest import mock

import pytest
from digitalhub.plugins import build_spec
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from digitalhub_runtime_tvm.entities.function.tvm.crud import new_function_tvm
from digitalhub_runtime_tvm.entities.function.tvm.spec import FunctionSpecTvm
from digitalhub_runtime_tvm.entities.model.tvm.models import TensorSpec
from digitalhub_runtime_tvm.entities.run.compile.spec import RunSpecTvmRunCompile
from digitalhub_runtime_tvm.entities.run.serve.spec import RunSpecTvmRunServe
from digitalhub_runtime_tvm.entities.task.serve.spec import TaskSpecTvmServe


def test_serve_spec_round_trip():
    options = {
        "function": "tvm://test/function:1",
        "task": "tvm+serve://test/task",
        "so_model_path": "store://test/model/tvm-so/model:version",
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
        function="tvm://test/function:1",
        task="tvm+serve://test/task",
        so_model_path="store://test/model/tvm-so/model:version",
    ).to_dict()
    assert spec == {
        "function": "tvm://test/function:1",
        "task": "tvm+serve://test/task",
        "so_model_path": "store://test/model/tvm-so/model:version",
        "inputs": {},
    }
    assert RunSpecTvmRunServe.model_validate(spec).model_dump(mode="json", exclude_none=True) == spec


@pytest.mark.parametrize(
    "so_model_path", [None, "", " ", "store://test/model/tvm-so/model", "store://test/model/tvm-ir/model:version"]
)
def test_serve_requires_a_versioned_compiled_model(so_model_path):
    with pytest.raises(ValidationError):
        RunSpecTvmRunServe(function="tvm://test/function:1", task="tvm+serve://test/task", so_model_path=so_model_path)


def test_serve_cannot_use_a_legacy_function_or_run_reference():
    with pytest.raises(ValidationError):
        RunSpecTvmRunServe(
            function="tvm://test/function:1",
            task="tvm+serve://test/task",
            so_model="store://test/model/tvm-so/model:old",
        )
    assert "so_model" not in FunctionSpecTvm.model_fields
    assert "so_model" not in RunSpecTvmRunServe.model_fields
    assert "so_model_path" not in TaskSpecTvmServe.model_fields


def test_legacy_function_and_run_snapshots_remain_readable_without_mutation():
    source = {"model": "store://test/model/onnx/model:v1", "so_model": "store://test/model/tvm-so/model:old"}
    function = FunctionSpecTvm.model_validate(source)
    assert "so_model" not in function.to_dict()
    assert source["so_model"] == "store://test/model/tvm-so/model:old"
    run = {
        "function": "tvm://test/function:1",
        "task": "tvm+serve://test/task",
        "model_path": "store://test/model/tvm-so/model:chosen",
        "so_model": source["so_model"],
    }
    parsed = RunSpecTvmRunServe.model_validate(run).to_dict()
    assert parsed["so_model_path"] == "store://test/model/tvm-so/model:chosen"
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
    "so_model_path",
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
def test_model_selection_matches_the_core_export(so_model_path):
    schema_dir = os.environ.get("TVM_CORE_SCHEMA_DIR")
    if not schema_dir:
        pytest.skip("CORE schema export directory not supplied")
    schema = json.loads((Path(schema_dir) / "run" / "tvm+serve:run.json").read_text())
    data = {"task": "tvm+serve://test/task", "function": "tvm://test/model:v1", "so_model_path": so_model_path}
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
        ("so_model_path", "/tmp/model"),
        ("so_model_path", "store://test/artifact/tvm-so/model:version"),
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
            {
                "function": "tvm://test/function:1",
                "task": "tvm+serve://test/task",
                "so_model_path": "store://test/model/tvm-so/model:version",
                field: value,
            }
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


@pytest.mark.parametrize(
    ("spec_cls", "kind", "field", "model_kind"),
    [
        (RunSpecTvmRunCompile, "compile", "ir_model_path", "tvm-ir"),
        (RunSpecTvmRunServe, "serve", "so_model_path", "tvm-so"),
    ],
)
def test_legacy_path_serializes_with_phase_name(spec_cls, kind, field, model_kind):
    key = f"store://test/model/{model_kind}/model:v1"
    legacy = {"function": "tvm://test/function:1", "task": f"tvm+{kind}://test/task", "model_path": key}
    for parsed in (
        spec_cls.from_dict(legacy),
        build_spec(spec_cls, **legacy),
        build_spec(spec_cls, **legacy, **{field: key}),
    ):
        stored = parsed.to_dict()
        assert stored[field] == key
        assert "model_path" not in stored
    assert field not in legacy
    with pytest.raises(ValueError, match="Conflicting"):
        build_spec(spec_cls, **legacy, **{field: key + "2"})
