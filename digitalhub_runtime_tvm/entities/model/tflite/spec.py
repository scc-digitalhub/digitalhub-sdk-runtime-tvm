# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.model._base.spec import ModelSpec

from digitalhub_runtime_tvm.entities.model.tvm.models import TensorSpec


class ModelSpecTflite(ModelSpec):
    """ModelSpecTflite specifications."""

    inputs: list[TensorSpec] | None = None
    outputs: list[TensorSpec] | None = None
