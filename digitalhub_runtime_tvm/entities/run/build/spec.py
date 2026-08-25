# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub_runtime_tvm.entities.run._base.spec import RunSpecTvmRun, RunValidatorTvmRun


class RunSpecTvmRunBuild(RunSpecTvmRun):
    """Tvm build run specifications."""


class RunValidatorTvmRunBuild(RunValidatorTvmRun):
    """Tvm build run validator."""
