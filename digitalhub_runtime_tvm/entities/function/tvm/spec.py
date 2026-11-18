# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Literal

from digitalhub.entities._base.entity.spec import Spec
from pydantic import Field

TvmFormat = Literal["auto", "onnx", "tflite"]


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

    so_model: str | None = None
    """Store key of the compiled model.so produced by compile."""


FunctionValidatorTvm = FunctionSpecTvm
