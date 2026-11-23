# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

import pytest
from digitalhub.entities._constructors.spec import build_spec
from pydantic import ValidationError

from digitalhub_runtime_tvm.entities.function.tvm.spec import FunctionSpecTvm, FunctionValidatorTvm
from digitalhub_runtime_tvm.entities.model.onnx.spec import ModelSpecOnnx, ModelValidatorOnnx
from digitalhub_runtime_tvm.entities.model.tflite.spec import ModelSpecTflite, ModelValidatorTflite
from digitalhub_runtime_tvm.entities.model.tvm.models import TensorSpec
from digitalhub_runtime_tvm.entities.model.tvm.spec import ModelSpecTvm, ModelValidatorTvm
from digitalhub_runtime_tvm.entities.model.tvm_ir.spec import ModelSpecTvmIr, ModelValidatorTvmIr
from digitalhub_runtime_tvm.entities.model.tvm_so.spec import ModelSpecTvmSo, ModelValidatorTvmSo
from digitalhub_runtime_tvm.entities.run._base.spec import RunSpecTvmRun, RunValidatorTvmRun
from digitalhub_runtime_tvm.entities.run.build.spec import RunSpecTvmRunBuild, RunValidatorTvmRunBuild
from digitalhub_runtime_tvm.entities.run.compile.models import TvmOptimization, TvmTuning
from digitalhub_runtime_tvm.entities.run.compile.spec import RunSpecTvmRunCompile, RunValidatorTvmRunCompile
from digitalhub_runtime_tvm.entities.run.serve.spec import RunSpecTvmRunServe, RunValidatorTvmRunServe
from digitalhub_runtime_tvm.entities.task.build.spec import TaskSpecTvmBuild, TaskValidatorTvmBuild
from digitalhub_runtime_tvm.entities.task.compile.spec import TaskSpecTvmCompile, TaskValidatorTvmCompile
from digitalhub_runtime_tvm.entities.task.serve.spec import TaskSpecTvmServe, TaskValidatorTvmServe


@pytest.mark.parametrize(
    ("compatibility_name", "spec_class"),
    [
        (FunctionValidatorTvm, FunctionSpecTvm),
        (TaskValidatorTvmBuild, TaskSpecTvmBuild),
        (TaskValidatorTvmServe, TaskSpecTvmServe),
        (TaskValidatorTvmCompile, TaskSpecTvmCompile),
        (RunValidatorTvmRun, RunSpecTvmRun),
        (RunValidatorTvmRunBuild, RunSpecTvmRunBuild),
        (RunValidatorTvmRunServe, RunSpecTvmRunServe),
        (RunValidatorTvmRunCompile, RunSpecTvmRunCompile),
        (ModelValidatorTvm, ModelSpecTvm),
        (ModelValidatorTvmIr, ModelSpecTvmIr),
        (ModelValidatorOnnx, ModelSpecOnnx),
        (ModelValidatorTflite, ModelSpecTflite),
        (ModelValidatorTvmSo, ModelSpecTvmSo),
    ],
)
def test_validator_names_are_spec_aliases(compatibility_name, spec_class):
    assert compatibility_name is spec_class


@pytest.mark.parametrize(
    ("spec_class", "action", "options"),
    [
        (RunSpecTvmRunBuild, "build", {}),
        (RunSpecTvmRunCompile, "compile", {"ir_model_path": "store://test/model/tvm-ir/model:v1"}),
        (RunSpecTvmRunServe, "serve", {"so_model_path": "store://test/model/tvm-so/model:v1"}),
    ],
)
def test_core_remote_run_responses_remain_readable(spec_class, action, options):
    snapshot = {"task": f"tvm+{action}://test/task", "local_execution": False, **options}
    parsed = spec_class.from_dict(snapshot)

    assert parsed.to_dict() == {"task": snapshot["task"], "inputs": {}, **options}
    assert snapshot["local_execution"] is False
    with pytest.raises(ValueError, match="only remote execution"):
        spec_class.from_dict({**snapshot, "local_execution": True})


def test_tvm_function_and_model_specs_use_typed_fields():
    function = build_spec(FunctionSpecTvm, model="store://project/model/onnx/input:v1", format="onnx")
    model = build_spec(
        ModelSpecOnnx,
        path="store://project/model/onnx/input:v1",
        inputs=[{"name": "features", "dtype": "float32", "shape": [1, 4]}],
        opset=17,
    )

    assert function.model == "store://project/model/onnx/input:v1"
    assert function.format == "onnx"
    assert isinstance(model.inputs[0], TensorSpec)
    assert model.inputs[0].shape == [1, 4]

    with pytest.raises(ValidationError):
        build_spec(ModelSpecOnnx, path="model", opset=0)


def test_tvm_compile_options_belong_to_the_run():
    historical = {"function": "function", "opt_level": 3, "tuning_trials": 1}
    task = TaskSpecTvmCompile.from_dict(historical)
    assert task.function == "function"
    assert "opt_level" not in task.to_dict()
    assert historical["opt_level"] == 3

    with pytest.raises(TypeError, match="opt_level"):
        build_spec(TaskSpecTvmCompile, **historical)


def test_tvm_compile_run_groups_flat_options_and_validates_target():
    run = build_spec(
        RunSpecTvmRunCompile,
        task="tvm+compile://task",
        target_architecture=" AMD64 ",
        opt_level=3,
        tuning_mode="off",
        tuning_trials=4,
    )

    assert run.target_architecture == "amd64"
    assert isinstance(run.optimization, TvmOptimization)
    assert run.optimization.opt_level == 3
    assert isinstance(run.tuning, TvmTuning)
    assert run.tuning.tuning_mode == "off"
    assert run.to_dict()["optimization"] == {"opt_level": 3}
    assert run.to_dict()["tuning"] == {"tuning_mode": "off", "tuning_trials": 4}

    grouped = build_spec(
        RunSpecTvmRunCompile,
        task="tvm+compile://task",
        opt_level=1,
        optimization={"opt_level": 2},
    )
    assert grouped.optimization.opt_level == 2

    with pytest.raises(ValidationError):
        build_spec(RunSpecTvmRunCompile, task="tvm+compile://task", opt_level=4)

    with pytest.raises(ValidationError):
        build_spec(RunSpecTvmRunCompile, task="tvm+compile://task", target={"kind": "cuda"})

    with pytest.raises(TypeError, match="unknown_option"):
        build_spec(RunSpecTvmRunCompile, task="tvm+compile://task", unknown_option=True)


def test_tvm_option_models_keep_strict_config_and_sdk_serialization():
    optimization = TvmOptimization(opt_level=3)
    tuning = TvmTuning(tuning_mode="off", tuning_trials=4)

    assert optimization.to_dict() == {"opt_level": 3}
    assert tuning.to_dict() == {"tuning_mode": "off", "tuning_trials": 4}

    with pytest.raises(ValidationError):
        TvmOptimization(opt_level=3, unknown_option=True)


def test_tvm_build_run_keeps_documented_run_options():
    run = build_spec(
        RunSpecTvmRunBuild,
        task="tvm+build://task",
        simplify=True,
        target_opset=18,
    )

    assert run.simplify is True
    assert run.target_opset == 18
