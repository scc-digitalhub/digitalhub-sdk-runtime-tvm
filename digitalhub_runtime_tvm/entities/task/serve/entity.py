# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.entities.task._base.entity import Task

if typing.TYPE_CHECKING:
    from digitalhub_runtime_tvm.entities.task.serve.spec import TaskSpecTvmServe
    from digitalhub_runtime_tvm.entities.task.serve.status import TaskStatusTvmServe


class TaskTvmServe(Task):
    """
    TaskTvmServe class.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: TaskSpecTvmServe
        self.status: TaskStatusTvmServe
