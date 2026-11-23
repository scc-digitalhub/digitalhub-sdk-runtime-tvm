# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
# SPDX-License-Identifier: Apache-2.0

import json
import os
from pathlib import Path

import pytest
from jsonschema.validators import validator_for

from digitalhub_runtime_tvm.entities.run.build.spec import RunSpecTvmRunBuild


@pytest.mark.parametrize("sort", [None, False, True])
@pytest.mark.parametrize("simplify", [None, False, True])
def test_build_flags_round_trip_independently(sort, simplify):
    options = {"task": "tvm+build://test/task", "function": "tvm://test/function:1"}
    if sort is not None:
        options["sort_onnx"] = sort
    if simplify is not None:
        options["simplify"] = simplify
    spec = RunSpecTvmRunBuild(**options).to_dict()
    assert spec == {**options, "inputs": {}}
    assert RunSpecTvmRunBuild.model_validate(spec).to_dict() == spec
    assert RunSpecTvmRunBuild(**spec).to_dict() == spec

    schema_dir = os.environ.get("TVM_CORE_SCHEMA_DIR")
    if schema_dir:
        schema = json.loads((Path(schema_dir) / "run" / "tvm+build:run.json").read_text())
        field = schema["properties"]["sort_onnx"]
        assert field["type"] == "boolean"
        assert field["default"] is False
        validator_for(schema)(schema).validate(spec)


def test_build_sort_option_is_declared_in_sdk_schema():
    assert RunSpecTvmRunBuild.model_json_schema()["properties"].get("sort_onnx")
