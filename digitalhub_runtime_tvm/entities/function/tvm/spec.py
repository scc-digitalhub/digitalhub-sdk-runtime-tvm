# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.plugins import Spec
from pydantic import Field, model_validator

from digitalhub_runtime_tvm.entities._commons.models import TvmFormat


class FunctionSpecTvm(Spec):
    """
    FunctionTvm specifications.
    """

    model: str
    """Source model path or store key."""

    format: TvmFormat | None = Field(default=None, json_schema_extra={"default": "auto"})
    """Source model format."""

    ir_model: str | None = None
    """Store key of the Relax IR model produced by build."""

    @model_validator(mode="before")
    @classmethod
    def ignore_legacy_compiled_model(cls, data):
        if isinstance(data, dict) and "so_model" in data:
            data = {key: value for key, value in data.items() if key != "so_model"}
        return data
