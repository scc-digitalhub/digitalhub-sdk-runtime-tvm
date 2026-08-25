# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.task._base.builder import TaskBuilder

from digitalhub_runtime_tvm.entities._base.runtime_entity.builder import RuntimeEntityBuilderTvm
from digitalhub_runtime_tvm.entities._commons.enums import EntityKinds
from digitalhub_runtime_tvm.entities.task.serve.entity import TaskTvmServe
from digitalhub_runtime_tvm.entities.task.serve.spec import TaskSpecTvmServe, TaskValidatorTvmServe
from digitalhub_runtime_tvm.entities.task.serve.status import TaskStatusTvmServe


class TaskTvmServeBuilder(TaskBuilder, RuntimeEntityBuilderTvm):
    """
    TaskTvmServeBuilder serveer.
    """

    ENTITY_CLASS = TaskTvmServe
    ENTITY_SPEC_CLASS = TaskSpecTvmServe
    ENTITY_SPEC_VALIDATOR = TaskValidatorTvmServe
    ENTITY_STATUS_CLASS = TaskStatusTvmServe
    ENTITY_KIND = EntityKinds.TASK_TVM_SERVE.value
