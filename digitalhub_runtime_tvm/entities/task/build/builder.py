# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.plugins import Status, TaskBuilder

from digitalhub_runtime_tvm.entities._base.runtime_entity.builder import RuntimeEntityBuilderTvm
from digitalhub_runtime_tvm.entities._commons.enums import EntityKinds
from digitalhub_runtime_tvm.entities.task.build.entity import TaskTvmBuild
from digitalhub_runtime_tvm.entities.task.build.spec import TaskSpecTvmBuild


class TaskTvmBuildBuilder(TaskBuilder, RuntimeEntityBuilderTvm):
    """
    TaskTvmBuild builder.
    """

    ENTITY_CLASS = TaskTvmBuild
    ENTITY_SPEC_CLASS = TaskSpecTvmBuild
    ENTITY_STATUS_CLASS = Status
    ENTITY_KIND = EntityKinds.TASK_TVM_BUILD.value
