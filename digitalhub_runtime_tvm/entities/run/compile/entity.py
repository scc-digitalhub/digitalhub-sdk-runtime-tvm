# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub_runtime_tvm.entities.run._base.entity import RunTvmRun

if typing.TYPE_CHECKING:
    from digitalhub_runtime_tvm.entities.run.compile.spec import RunSpecTvmRunCompile
    from digitalhub_runtime_tvm.entities.run.compile.status import RunStatusTvmRunCompile


class RunTvmRunCompile(RunTvmRun):
    """
    RunTvmRunCompile class.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: RunSpecTvmRunCompile
        self.status: RunStatusTvmRunCompile
