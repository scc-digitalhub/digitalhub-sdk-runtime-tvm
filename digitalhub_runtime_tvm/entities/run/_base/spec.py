# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub.entities.run._base.spec import RunSpecFunction
from pydantic import Field, field_validator

from digitalhub_runtime_tvm.entities._commons.models import TvmFormat


class RunSpecTvmRun(RunSpecFunction):
    """
    Tvm run specifications.
    """

    model: str | None = None
    inputs: dict[str, str] = Field(default_factory=dict)
    format: TvmFormat | None = Field(default=None, json_schema_extra={"default": "auto"})
    ir_model: str | None = None
    so_model: str | None = None

    @field_validator("inputs", mode="before")
    @classmethod
    def default_inputs(cls, value):
        return {} if value is None else value
