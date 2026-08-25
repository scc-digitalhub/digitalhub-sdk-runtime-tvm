# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0
from digitalhub_runtime_tvm.entities._commons.enums import EntityKinds
from digitalhub_runtime_tvm.entities.function.tvm.builder import FunctionTvmBuilder
from digitalhub_runtime_tvm.entities.run.build.builder import RunTvmRunBuildBuilder
from digitalhub_runtime_tvm.entities.run.compile.builder import RunTvmRunCompileBuilder
from digitalhub_runtime_tvm.entities.run.serve.builder import RunTvmRunServeBuilder
from digitalhub_runtime_tvm.entities.task.build.builder import TaskTvmBuildBuilder
from digitalhub_runtime_tvm.entities.task.compile.builder import TaskTvmCompileBuilder
from digitalhub_runtime_tvm.entities.task.serve.builder import TaskTvmServeBuilder

entity_builders = (
    (EntityKinds.FUNCTION_TVM.value, FunctionTvmBuilder),
    (EntityKinds.TASK_TVM_BUILD.value, TaskTvmBuildBuilder),
    (EntityKinds.TASK_TVM_COMPILE.value, TaskTvmCompileBuilder),
    (EntityKinds.TASK_TVM_SERVE.value, TaskTvmServeBuilder),
    (EntityKinds.RUN_TVM_BUILD.value, RunTvmRunBuildBuilder),
    (EntityKinds.RUN_TVM_COMPILE.value, RunTvmRunCompileBuilder),
    (EntityKinds.RUN_TVM_SERVE.value, RunTvmRunServeBuilder),
)

try:
    from digitalhub_runtime_tvm.runtimes.builder import RuntimeTvmBuilder

    runtime_builders = ((kind, RuntimeTvmBuilder) for kind in [e.value for e in EntityKinds])
except ImportError as e:
    from digitalhub.utils.logger.logger import get_logger

    logger = get_logger(__name__)
    logger.debug(f"Error importing runtime builders: {e}")
    runtime_builders = ()
