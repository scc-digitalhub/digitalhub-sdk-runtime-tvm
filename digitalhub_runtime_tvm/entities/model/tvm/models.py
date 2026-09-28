# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from pydantic import BaseModel


class TensorSpec(BaseModel):
    """TVM model tensor input/output signature."""

    name: str | None = None
    dtype: str | None = None
    shape: list[int] | None = None
    scale: list[float] | None = None
    zero_point: list[int] | None = None
    quantized_dimension: int | None = None

    def to_dict(self):
        return self.model_dump()
