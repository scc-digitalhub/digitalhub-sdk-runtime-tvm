# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

import pytest
from digitalhub.entities._constructors.spec import build_spec
from pydantic import ValidationError

from digitalhub_runtime_tvm.entities._mixin.execution.spec import TvmBuildSpecMixin, TvmServeSpecMixin
from digitalhub_runtime_tvm.entities.function.tvm.spec import FunctionSpecTvm
from digitalhub_runtime_tvm.entities.model.onnx.spec import ModelSpecOnnx
from digitalhub_runtime_tvm.entities.model.tvm.models import TensorSpec
from digitalhub_runtime_tvm.entities.run.build.spec import RunSpecTvmRunBuild
from digitalhub_runtime_tvm.entities.run.compile.models import TvmOptimization, TvmTuning
from digitalhub_runtime_tvm.entities.run.compile.spec import RunSpecTvmRunCompile
from digitalhub_runtime_tvm.entities.run.serve.spec import RunSpecTvmRunServe
from digitalhub_runtime_tvm.entities.task.build.spec import TaskSpecTvmBuild
from digitalhub_runtime_tvm.entities.task.compile.spec import TaskSpecTvmCompile
from digitalhub_runtime_tvm.entities.task.serve.spec import TaskSpecTvmServe


def test_tvm_action_mixins_have_one_runtime_owner():
    assert TvmBuildSpecMixin not in TaskSpecTvmBuild.__mro__
    assert TvmBuildSpecMixin in RunSpecTvmRunBuild.__mro__
    assert TvmServeSpecMixin not in TaskSpecTvmServe.__mro__
    assert TvmServeSpecMixin in RunSpecTvmRunServe.__mro__


@pytest.mark.parametrize(
    ("spec_class", "action", "options"),
    [
        (RunSpecTvmRunBuild, "build", {}),
        (RunSpecTvmRunCompile, "compile", {"ir_model_path": "store://test/model/tvm-ir/model:v1"}),
        (RunSpecTvmRunServe, "serve", {"so_model_path": "store://test/model/tvm-so/model:v1"}),
    ],
)
def test_core_remote_run_responses_remain_readable(spec_class, action, options):
    snapshot = {
        "function": "tvm://test/function:1",
        "task": f"tvm+{action}://test/task",
        "local_execution": False,
        **options,
    }
    parsed = spec_class.from_dict(snapshot)

    assert parsed.to_dict() == {"function": "tvm://test/function:1", "task": snapshot["task"], "inputs": {}, **options}
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
        function="function",
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
        function="function",
        task="tvm+compile://task",
        opt_level=1,
        optimization={"opt_level": 2},
    )
    assert grouped.optimization.opt_level == 2

    with pytest.raises(ValidationError):
        build_spec(
            RunSpecTvmRunCompile,
            function="function",
            task="tvm+compile://task",
            opt_level=4,
        )

    with pytest.raises(ValidationError):
        build_spec(
            RunSpecTvmRunCompile,
            function="function",
            task="tvm+compile://task",
            target={"kind": "cuda"},
        )

    with pytest.raises(TypeError, match="unknown_option"):
        build_spec(
            RunSpecTvmRunCompile,
            function="function",
            task="tvm+compile://task",
            unknown_option=True,
        )


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
        function="function",
        task="tvm+build://task",
        simplify=True,
        target_opset=18,
    )

    assert run.simplify is True
    assert run.target_opset == 18
