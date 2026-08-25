# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub.entities.run._base.spec import RunSpec, RunValidator


class RunSpecTvmRun(RunSpec):
    """Tvm run specifications."""


class RunValidatorTvmRun(RunValidator):
    """Tvm run validator."""
