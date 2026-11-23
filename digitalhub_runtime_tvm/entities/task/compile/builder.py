# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities._base.entity.status import Status
from digitalhub.entities.task._base.builder import TaskBuilder

from digitalhub_runtime_tvm.entities._base.runtime_entity.builder import RuntimeEntityBuilderTvm
from digitalhub_runtime_tvm.entities._commons.enums import EntityKinds
from digitalhub_runtime_tvm.entities.task.compile.entity import TaskTvmCompile
from digitalhub_runtime_tvm.entities.task.compile.spec import TaskSpecTvmCompile


class TaskTvmCompileBuilder(TaskBuilder, RuntimeEntityBuilderTvm):
    """
    TaskTvmCompileBuilder compileer.
    """

    ENTITY_CLASS = TaskTvmCompile
    ENTITY_SPEC_CLASS = TaskSpecTvmCompile
    ENTITY_STATUS_CLASS = Status
    ENTITY_KIND = EntityKinds.TASK_TVM_COMPILE.value
