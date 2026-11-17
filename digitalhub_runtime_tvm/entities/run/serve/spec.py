# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from pydantic import Field

from digitalhub_runtime_tvm.entities.run._base.spec import RunSpecTvmRun
from digitalhub_runtime_tvm.entities.task.serve.spec import TvmServeSpecMixin


class RunSpecTvmRunServe(RunSpecTvmRun, TvmServeSpecMixin):
    """
    Tvm serve run specifications.
    """

    model_path: str = Field(pattern=r"^store://[^/]+/model/tvm-so/[^/:]+:[^/]+$")


class RunValidatorTvmRunServe(RunSpecTvmRunServe):
    """Compatibility name for the typed TVM serve-run spec."""
