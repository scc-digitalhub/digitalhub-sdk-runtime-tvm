# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub_runtime_tvm.entities.run._base.entity import RunTvmRun

if typing.TYPE_CHECKING:
    from digitalhub_runtime_tvm.entities.run.build.spec import RunSpecTvmRunBuild
    from digitalhub_runtime_tvm.entities.run.build.status import RunStatusTvmRunBuild


class RunTvmRunBuild(RunTvmRun):
    """
    RunTvmRunBuild class.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: RunSpecTvmRunBuild
        self.status: RunStatusTvmRunBuild
