# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub_runtime_tvm.entities.run._base.spec import RunSpecTvmRun
from digitalhub_runtime_tvm.entities.task.build.spec import TvmBuildSpecMixin


class RunSpecTvmRunBuild(RunSpecTvmRun, TvmBuildSpecMixin):
    """
    Tvm build run specifications.
    """


class RunValidatorTvmRunBuild(RunSpecTvmRunBuild):
    """Compatibility name for the typed TVM build-run spec."""
