# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Literal

from digitalhub.entities.function._base.spec import FunctionSpec, FunctionValidator

TvmFormat = Literal["auto", "onnx", "tflite"]


class FunctionSpecTvm(FunctionSpec):
    """
    FunctionTvm specifications.
    """

    def __init__(
        self,
        model: str,
        format: TvmFormat | None = None,
        ir_model: str | None = None,
        so_model: str | None = None,
    ) -> None:
        super().__init__()
        self.model = model
        self.format = format
        self.ir_model = ir_model
        self.so_model = so_model


class FunctionValidatorTvm(FunctionValidator):
    """
    FunctionTvm validator.
    """

    model: str
    """Source model path or store key."""

    format: TvmFormat | None = None
    """Source model format."""

    ir_model: str | None = None
    """Store key of the Relax IR model produced by build."""

    so_model: str | None = None
    """Store key of the compiled model.so produced by compile."""
