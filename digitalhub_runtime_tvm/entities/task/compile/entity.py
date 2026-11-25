# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.plugins import Task

if typing.TYPE_CHECKING:
    from digitalhub.plugins import Status

    from digitalhub_runtime_tvm.entities.task.compile.spec import TaskSpecTvmCompile


class TaskTvmCompile(Task):
    """
    TaskTvmCompile class.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: TaskSpecTvmCompile
        self.status: Status
