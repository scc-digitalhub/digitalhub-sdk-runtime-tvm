# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

import json
import os
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import ValidationError as SchemaValidationError
from jsonschema.validators import validator_for
from pydantic import ValidationError

from digitalhub_runtime_tvm.entities.run.compile.spec import RunSpecTvmRunCompile


@pytest.fixture(scope="module", params=["sdk", "core"])
def compile_schema(request):
    if request.param == "sdk":
        schema = RunSpecTvmRunCompile.model_json_schema()
    else:
        root = Path(os.environ.get("TVM_CORE_SCHEMA_DIR", Path(__file__).parent / "instances" / "schemas"))
        path = root / "run" / "tvm+compile:run.json"
        if not path.exists():
            if os.environ.get("TVM_REQUIRE_CORE_SCHEMAS") == "1":
                pytest.fail(f"Required CORE schema export is missing: {path}")
            pytest.skip("CORE schema export is not available under test/instances/schemas")
        schema = json.loads(path.read_text())
    validator = validator_for(schema)
    validator.check_schema(schema)
    return validator(schema)


def cuda_target():
    return {
        "kind": "cuda",
        "arch": "sm_87",
        "host": {"kind": "llvm", "mtriple": "aarch64-linux-gnu"},
    }


def test_legacy_compile_snapshot_ignores_saved_function_model():
    snapshot = {
        "function": "tvm://test/function:1",
        "task": "tvm+compile://test/task",
        "so_model": "store://test/model/tvm-so/model:old",
    }
    expected = {"function": "tvm://test/function:1", "task": snapshot["task"], "inputs": {}}
    assert RunSpecTvmRunCompile.model_validate(snapshot).to_dict() == expected
    assert RunSpecTvmRunCompile(**snapshot).to_dict() == expected
    assert "so_model" in snapshot


def test_cuda_compile_round_trip_preserves_target_options_and_job_settings(compile_schema):
    target = cuda_target()
    target.update(
        {
            "max_threads_per_block": 1024,
            "max_shared_memory_per_block": 49152,
            "thread_warp_size": 32,
            "keys": ["cuda", "gpu"],
            "libs": ["cublas"],
        }
    )
    target["host"].update(
        {
            "mcpu": "cortex-a78",
            "mattr": ["+neon"],
            "mfloat-abi": "hard",
            "num-cores": 6,
            "keys": ["arm_cpu", "cpu"],
            "opt-level": 3,
        }
    )
    options = {
        "task": "tvm+compile://test/task",
        "function": "tvm://test/function:1",
        "target": target,
        "image": "example/tvm-cuda:custom",
        "resources": {"cpu": "6", "mem": "8Gi", "gpu": "1"},
        "profile": "jetson-orin",
        "envs": [{"name": "TVM_LOG_LEVEL", "value": "INFO"}],
        "optimization": {"cross_cc": "aarch64-linux-gnu-g++", "cross_cc_options": ["--sysroot=/opt/arm64"]},
        "tuning": {"tuning_mode": "off"},
    }
    original = deepcopy(options)
    spec = RunSpecTvmRunCompile(**options).to_dict()
    assert spec == {**original, "inputs": {}}
    assert RunSpecTvmRunCompile.model_validate(spec).to_dict() == spec
    assert RunSpecTvmRunCompile(**spec).to_dict() == spec
    assert options == original
    compile_schema.validate(spec)


@pytest.mark.parametrize("arch", ["sm_75", "sm_87", "sm_90a", "sm_100f"])
@pytest.mark.parametrize(
    "triple",
    [
        "x86_64-linux-gnu",
        "x86_64-pc-linux-gnu",
        "amd64-unknown-linux-gnu",
        "aarch64-linux-gnu",
        "aarch64-unknown-linux-gnu",
        "arm64-linux-gnu",
    ],
)
def test_cuda_requires_explicit_supported_device_and_host(arch, triple, compile_schema):
    target = cuda_target()
    target["arch"] = arch
    target["host"]["mtriple"] = triple
    spec = RunSpecTvmRunCompile(
        task="tvm+compile://test/task", function="tvm://test/function:1", target=target
    ).to_dict()
    assert spec["target"] == target
    compile_schema.validate(spec)


@pytest.mark.parametrize(
    ("path", "value"),
    [
        (("kind",), "opencl"),
        (("arch",), None),
        (("arch",), 87),
        (("arch",), ""),
        (("arch",), "cuda"),
        (("arch",), "sm_87 "),
        (("arch",), "compute_87"),
        (("arch",), "sm_90aa"),
        (("host",), None),
        (("host",), "llvm -mtriple=aarch64-linux-gnu"),
        (("host",), {}),
        (("host", "kind"), "cuda"),
        (("host", "mtriple"), None),
        (("host", "mtriple"), ""),
        (("host", "mtriple"), "aarch64"),
        (("host", "mtriple"), "aarch64-linux-musl"),
        (("host", "mtriple"), "armv7-linux-gnueabihf"),
        (("host", "mtriple"), "i686-linux-gnu"),
        (("host", "mtriple"), "x86_64-w64-mingw32"),
        (("host", "mtriple"), "x86_64-apple-darwin"),
        (("host", "mcpu"), 72),
        (("host", "mfloat-abi"), False),
        (("host", "mattr"), "+neon"),
        (("host", "mattr"), ["+neon", 1]),
        (("host", "num-cores"), True),
        (("host", "num-cores"), 0),
        (("max_threads_per_block",), 0),
        (("max_shared_memory_per_block",), "49152"),
        (("thread_warp_size",), True),
    ],
)
def test_invalid_cuda_targets_are_rejected_by_validator_and_schema(path, value, compile_schema):
    target = cuda_target()
    parent = target
    for name in path[:-1]:
        parent = parent[name]
    parent[path[-1]] = value
    options = {"task": "tvm+compile://test/task", "function": "tvm://test/function:1", "target": target}
    with pytest.raises(ValidationError):
        RunSpecTvmRunCompile.model_validate(options)
    with pytest.raises(SchemaValidationError) as error:
        compile_schema.validate(options)
    assert error.value.absolute_path[0] == "target"


@pytest.mark.parametrize("path", [("kind",), ("arch",), ("host",), ("host", "kind"), ("host", "mtriple")])
def test_cuda_target_cannot_omit_device_or_host_details(path, compile_schema):
    target = cuda_target()
    parent = target
    for name in path[:-1]:
        parent = parent[name]
    del parent[path[-1]]
    options = {"task": "tvm+compile://test/task", "function": "tvm://test/function:1", "target": target}
    with pytest.raises(ValidationError):
        RunSpecTvmRunCompile.model_validate(options)
    with pytest.raises(SchemaValidationError) as error:
        compile_schema.validate(options)
    assert error.value.absolute_path[0] == "target"


@pytest.mark.parametrize("target", [{"kind": "llvm"}, cuda_target()])
def test_explicit_targets_are_exclusive_with_configured_profiles(target):
    with pytest.raises(ValidationError, match="Use target or target_architecture"):
        RunSpecTvmRunCompile(
            function="tvm://test/function:1",
            task="tvm+compile://test/task",
            target=target,
            target_architecture="jetson_orin_cuda",
        )
    spec = RunSpecTvmRunCompile(
        function="tvm://test/function:1", task="tvm+compile://test/task", target=target, target_architecture=" AUTO "
    ).to_dict()
    assert spec["target_architecture"] == "auto"
    assert spec["target"] == target


@pytest.mark.parametrize("target", [None, {}, {"kind": "llvm"}, {"kind": "llvm", "mcpu": "native", "libs": ["m"]}])
def test_cpu_targets_keep_optional_triples_and_existing_options(target, compile_schema):
    options = {"task": "tvm+compile://test/task", "function": "tvm://test/function:1"}
    if target is not None:
        options["target"] = target
    spec = RunSpecTvmRunCompile(**options).to_dict()
    assert spec == {**options, "inputs": {}}
    compile_schema.validate(spec)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("mtriple", 64),
        ("mcpu", False),
        ("mfloat-abi", []),
        ("mattr", "+neon"),
        ("mattr", ["+neon", 1]),
        ("num-cores", True),
        ("num-cores", 0),
    ],
)
def test_invalid_cpu_target_options_keep_existing_validation(field, value):
    options = {
        "task": "tvm+compile://test/task",
        "function": "tvm://test/function:1",
        "target": {"kind": "llvm", field: value},
    }
    with pytest.raises(ValidationError):
        RunSpecTvmRunCompile.model_validate(options)
    schema = RunSpecTvmRunCompile.model_json_schema()
    validator = validator_for(schema)(schema)
    with pytest.raises(SchemaValidationError) as error:
        validator.validate(options)
    assert error.value.absolute_path[0] == "target"


def test_configured_profile_names_remain_open_and_compile_defaults_are_not_invented():
    options = {
        "function": "tvm://test/function:1",
        "task": "tvm+compile://test/task",
        "target_architecture": "  JETSON_ORIN_CUDA  ",
    }
    assert RunSpecTvmRunCompile(**options).to_dict() == {
        "function": "tvm://test/function:1",
        "task": options["task"],
        "inputs": {},
        "target_architecture": "jetson_orin_cuda",
    }
    assert RunSpecTvmRunCompile(function="tvm://test/function:1", task=options["task"]).to_dict() == {
        "function": "tvm://test/function:1",
        "task": options["task"],
        "inputs": {},
    }


@pytest.mark.parametrize("profile", ["auto", "cpu", "llvm"])
def test_explicit_target_accepts_auto_aliases(profile, compile_schema):
    spec = RunSpecTvmRunCompile(
        task="tvm+compile://test/task",
        function="tvm://test/function:1",
        target=cuda_target(),
        target_architecture=profile,
    ).to_dict()
    compile_schema.validate(spec)


@pytest.mark.parametrize("mode", ["off", "apply"])
def test_inactive_tuning_values_survive_both_schemas(mode, compile_schema):
    tuning = {
        "tuning_mode": mode,
        "tuning_trials": "dormant",
        "rpc_tracker_port": -1,
        "tuning_model_path": "s3://test/database",
    }
    spec = RunSpecTvmRunCompile(
        task="tvm+compile://test/task", function="tvm://test/function:1", tuning=tuning
    ).to_dict()
    assert spec["tuning"] == tuning
    compile_schema.validate(spec)
    schema = RunSpecTvmRunCompile.model_json_schema()
    validator_for(schema)(schema).validate(spec)


@pytest.mark.parametrize("change", ["missing_limits", "cache_flush", "blank_rpc", "bad_port"])
def test_active_cuda_tuning_rejected_consistently(change, compile_schema):
    target = cuda_target()
    target.update(max_shared_memory_per_block=49152, max_threads_per_block=1024, thread_warp_size=32)
    tuning = {"tuning_mode": "tune", "tuning_trials": 8}
    if change == "missing_limits":
        del target["thread_warp_size"]
    elif change == "cache_flush":
        tuning["tuning_enable_cpu_cache_flush"] = True
    else:
        tuning.update(tuning_runner="rpc", rpc_tracker_host="tracker", rpc_tracker_key="gpu", rpc_tracker_port=9190)
        tuning["rpc_tracker_key" if change == "blank_rpc" else "rpc_tracker_port"] = (
            "   " if change == "blank_rpc" else 65536
        )
    spec = {"task": "tvm+compile://test/task", "function": "tvm://test/function:1", "target": target, "tuning": tuning}
    with pytest.raises(ValidationError):
        RunSpecTvmRunCompile.model_validate(spec)
    with pytest.raises(SchemaValidationError):
        compile_schema.validate(spec)
    schema = RunSpecTvmRunCompile.model_json_schema()
    with pytest.raises(SchemaValidationError):
        validator_for(schema)(schema).validate(spec)


def test_integral_cuda_numbers_are_normalized(compile_schema):
    target = cuda_target()
    target["thread_warp_size"] = 32.0
    target["host"]["num-cores"] = 4.0
    spec = RunSpecTvmRunCompile(
        task="tvm+compile://test/task", function="tvm://test/function:1", target=target
    ).to_dict()
    assert type(spec["target"]["thread_warp_size"]) is int
    assert type(spec["target"]["host"]["num-cores"]) is int
    compile_schema.validate(spec)
