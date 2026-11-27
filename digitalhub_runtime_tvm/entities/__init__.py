# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub.plugins import (
    Action,
    BuilderDef,
    CrudPlugin,
    ExecFamily,
    ExecutableActions,
    FunctionBuilder,
    ModelBuilder,
    ModelStatus,
    Run,
    RunBuilder,
    RunStatus,
    Status,
    Task,
    TaskBuilder,
)

from digitalhub_runtime_tvm.entities._commons.enums import Actions, EntityKinds
from digitalhub_runtime_tvm.entities.function.tvm.crud import new_function_tvm
from digitalhub_runtime_tvm.entities.function.tvm.entity import FunctionTvm
from digitalhub_runtime_tvm.entities.function.tvm.spec import FunctionSpecTvm
from digitalhub_runtime_tvm.entities.model.onnx.crud import log_onnx, register_onnx
from digitalhub_runtime_tvm.entities.model.onnx.entity import ModelOnnx
from digitalhub_runtime_tvm.entities.model.onnx.spec import ModelSpecOnnx
from digitalhub_runtime_tvm.entities.model.tflite.crud import log_tflite, register_tflite
from digitalhub_runtime_tvm.entities.model.tflite.entity import ModelTflite
from digitalhub_runtime_tvm.entities.model.tflite.spec import ModelSpecTflite
from digitalhub_runtime_tvm.entities.model.tvm_ir.crud import log_tvm_ir, register_tvm_ir
from digitalhub_runtime_tvm.entities.model.tvm_ir.entity import ModelTvmIr
from digitalhub_runtime_tvm.entities.model.tvm_ir.spec import ModelSpecTvmIr
from digitalhub_runtime_tvm.entities.model.tvm_so.crud import log_tvm_so, register_tvm_so
from digitalhub_runtime_tvm.entities.model.tvm_so.entity import ModelTvmSo
from digitalhub_runtime_tvm.entities.model.tvm_so.spec import ModelSpecTvmSo
from digitalhub_runtime_tvm.entities.run.build.spec import RunSpecTvmRunBuild
from digitalhub_runtime_tvm.entities.run.compile.spec import RunSpecTvmRunCompile
from digitalhub_runtime_tvm.entities.run.serve.entity import RunTvmRunServe
from digitalhub_runtime_tvm.entities.run.serve.spec import RunSpecTvmRunServe
from digitalhub_runtime_tvm.entities.task.build.spec import TaskSpecTvmBuild
from digitalhub_runtime_tvm.entities.task.compile.spec import TaskSpecTvmCompile
from digitalhub_runtime_tvm.entities.task.serve.spec import TaskSpecTvmServe

# Imported on first use: the entities register even when the runtime cannot be
# imported, and the import error is reported when a run executes locally.
RUNTIME_TVM_BUILDER = "digitalhub_runtime_tvm.runtimes.builder:RuntimeTvmBuilder"

tvm = ExecFamily(
    executable=BuilderDef(
        EntityKinds.FUNCTION_TVM,
        FunctionTvm,
        FunctionSpecTvm,
        Status,
        base=FunctionBuilder,
        shortcuts=(CrudPlugin(new_function_tvm),),
    ),
    actions={
        ExecutableActions.BUILD: Action(
            task=BuilderDef(EntityKinds.TASK_TVM_BUILD, Task, TaskSpecTvmBuild, Status, base=TaskBuilder),
            run=BuilderDef(EntityKinds.RUN_TVM_BUILD, Run, RunSpecTvmRunBuild, RunStatus, base=RunBuilder),
        ),
        Actions.COMPILE: Action(
            task=BuilderDef(EntityKinds.TASK_TVM_COMPILE, Task, TaskSpecTvmCompile, Status, base=TaskBuilder),
            run=BuilderDef(EntityKinds.RUN_TVM_COMPILE, Run, RunSpecTvmRunCompile, RunStatus, base=RunBuilder),
        ),
        ExecutableActions.SERVE: Action(
            task=BuilderDef(EntityKinds.TASK_TVM_SERVE, Task, TaskSpecTvmServe, Status, base=TaskBuilder),
            run=BuilderDef(EntityKinds.RUN_TVM_SERVE, RunTvmRunServe, RunSpecTvmRunServe, RunStatus, base=RunBuilder),
        ),
    },
    runtime_builder=RUNTIME_TVM_BUILDER,
)

_models = (
    BuilderDef(
        EntityKinds.MODEL_ONNX,
        ModelOnnx,
        ModelSpecOnnx,
        ModelStatus,
        base=ModelBuilder,
        shortcuts=(
            CrudPlugin(log_onnx),
            CrudPlugin(register_onnx),
        ),
    ),
    BuilderDef(
        EntityKinds.MODEL_TFLITE,
        ModelTflite,
        ModelSpecTflite,
        ModelStatus,
        base=ModelBuilder,
        shortcuts=(
            CrudPlugin(log_tflite),
            CrudPlugin(register_tflite),
        ),
    ),
    BuilderDef(
        EntityKinds.MODEL_TVM_IR,
        ModelTvmIr,
        ModelSpecTvmIr,
        ModelStatus,
        base=ModelBuilder,
        shortcuts=(
            CrudPlugin(log_tvm_ir),
            CrudPlugin(register_tvm_ir),
        ),
    ),
    BuilderDef(
        EntityKinds.MODEL_TVM_SO,
        ModelTvmSo,
        ModelSpecTvmSo,
        ModelStatus,
        base=ModelBuilder,
        shortcuts=(
            CrudPlugin(log_tvm_so),
            CrudPlugin(register_tvm_so),
        ),
    ),
)

entity_plugins = (
    *(definition.plugin() for definition in _models),
    *tvm.plugins(),
)
