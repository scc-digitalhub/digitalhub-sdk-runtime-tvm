# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub_runtime_tvm.entities.run._base.entity import RunTvmRun

if typing.TYPE_CHECKING:
    from digitalhub.plugins import RunStatus

    from digitalhub_runtime_tvm.entities.run.serve.spec import RunSpecTvmRunServe


class RunTvmRunServe(RunTvmRun):
    """
    RunTvmRunServe class.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: RunSpecTvmRunServe
        self.status: RunStatus
