# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities._base.entity.status import Status
from digitalhub.entities.task._base.builder import TaskBuilder

from digitalhub_runtime_tvm.entities._base.runtime_entity.builder import RuntimeEntityBuilderTvm
from digitalhub_runtime_tvm.entities._commons.enums import EntityKinds
from digitalhub_runtime_tvm.entities.task.serve.entity import TaskTvmServe
from digitalhub_runtime_tvm.entities.task.serve.spec import TaskSpecTvmServe


class TaskTvmServeBuilder(TaskBuilder, RuntimeEntityBuilderTvm):
    """
    TaskTvmServeBuilder serveer.
    """

    ENTITY_CLASS = TaskTvmServe
    ENTITY_SPEC_CLASS = TaskSpecTvmServe
    ENTITY_STATUS_CLASS = Status
    ENTITY_KIND = EntityKinds.TASK_TVM_SERVE.value
