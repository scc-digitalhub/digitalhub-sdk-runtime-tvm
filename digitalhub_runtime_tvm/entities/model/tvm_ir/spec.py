# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Literal

from digitalhub_runtime_tvm.entities.model.tvm.spec import ModelSpecTvm

TvmSourceFormat = Literal["auto", "onnx", "tflite"]


class ModelSpecTvmIr(ModelSpecTvm):
    """ModelSpecTvmIr specifications."""

    source_format: TvmSourceFormat | None = None
    keep_params_in_input: bool | None = None
    sanitize_input_names: bool | None = None
