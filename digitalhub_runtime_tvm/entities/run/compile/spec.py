# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub_runtime_tvm.entities.run._base.spec import RunSpecTvmRun, RunValidatorTvmRun


class RunSpecTvmRunCompile(RunSpecTvmRun):
    """Tvm compile run specifications."""


class RunValidatorTvmRunCompile(RunValidatorTvmRun):
    """Tvm compile run validator."""
