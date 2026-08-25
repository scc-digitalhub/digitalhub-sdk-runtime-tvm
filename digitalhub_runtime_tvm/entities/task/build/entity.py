# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.entities.task._base.entity import Task

if typing.TYPE_CHECKING:
    from digitalhub_runtime_tvm.entities.task.build.spec import TaskSpecTvmBuild
    from digitalhub_runtime_tvm.entities.task.build.status import TaskStatusTvmBuild


class TaskTvmBuild(Task):
    """
    TaskTvmBuild class.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: TaskSpecTvmBuild
        self.status: TaskStatusTvmBuild
