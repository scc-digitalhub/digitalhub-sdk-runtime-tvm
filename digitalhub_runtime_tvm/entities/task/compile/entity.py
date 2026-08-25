# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.entities.task._base.entity import Task

if typing.TYPE_CHECKING:
    from digitalhub_runtime_tvm.entities.task.compile.spec import TaskSpecTvmCompile
    from digitalhub_runtime_tvm.entities.task.compile.status import TaskStatusTvmCompile


class TaskTvmCompile(Task):
    """
    TaskTvmCompile class.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: TaskSpecTvmCompile
        self.status: TaskStatusTvmCompile
