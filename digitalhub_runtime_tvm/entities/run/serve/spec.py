# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub_runtime_tvm.entities._mixin.execution.spec import TvmServeSpecMixin
from digitalhub_runtime_tvm.entities.run._base.spec import RunSpecTvmRun


class RunSpecTvmRunServe(RunSpecTvmRun, TvmServeSpecMixin):
    """
    Tvm serve run specifications.
    """
