# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from pydantic import model_validator

from digitalhub_runtime_tvm.entities._mixin.execution.spec import TvmServeSpecMixin
from digitalhub_runtime_tvm.entities.run._base.spec import RunSpecTvmRun, normalize_model_path


class RunSpecTvmRunServe(RunSpecTvmRun, TvmServeSpecMixin):
    """
    Tvm serve run specifications.
    """

    @model_validator(mode="before")
    @classmethod
    def read_legacy_path(cls, data):
        return normalize_model_path(data, "so_model_path") if isinstance(data, dict) else data
