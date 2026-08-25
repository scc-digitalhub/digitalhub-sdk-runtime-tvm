# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.entities.run._base.entity import Run

if typing.TYPE_CHECKING:
    from digitalhub_runtime_tvm.entities.run._base.spec import RunSpecTvmRun
    from digitalhub_runtime_tvm.entities.run._base.status import RunStatusTvmRun


class RunTvmRun(Run):
    """
    RunTvmRun class.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: RunSpecTvmRun
        self.status: RunStatusTvmRun
