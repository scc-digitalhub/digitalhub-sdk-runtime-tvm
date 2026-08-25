# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.task._base.builder import TaskBuilder

from digitalhub_runtime_tvm.entities._base.runtime_entity.builder import RuntimeEntityBuilderTvm
from digitalhub_runtime_tvm.entities._commons.enums import EntityKinds
from digitalhub_runtime_tvm.entities.task.build.entity import TaskTvmBuild
from digitalhub_runtime_tvm.entities.task.build.spec import (
    TaskSpecTvmBuild,
    TaskValidatorTvmBuild,
)
from digitalhub_runtime_tvm.entities.task.build.status import TaskStatusTvmBuild


class TaskTvmBuildBuilder(TaskBuilder, RuntimeEntityBuilderTvm):
    """
    TaskTvmBuild builder.
    """

    ENTITY_CLASS = TaskTvmBuild
    ENTITY_SPEC_CLASS = TaskSpecTvmBuild
    ENTITY_SPEC_VALIDATOR = TaskValidatorTvmBuild
    ENTITY_STATUS_CLASS = TaskStatusTvmBuild
    ENTITY_KIND = EntityKinds.TASK_TVM_BUILD.value
