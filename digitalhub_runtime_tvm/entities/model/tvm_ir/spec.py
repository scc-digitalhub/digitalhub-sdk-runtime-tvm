# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Literal

from digitalhub_runtime_tvm.entities.model.tvm.spec import ModelSpecTvm, ModelValidatorTvm

TvmSourceFormat = Literal["auto", "onnx", "tflite"]


class ModelSpecTvmIr(ModelSpecTvm):
    """ModelSpecTvmIr specifications."""

    def __init__(
        self,
        path: str,
        framework: str | None = None,
        algorithm: str | None = None,
        parameters: dict | None = None,
        entry: str | None = None,
        inputs: list[dict] | None = None,
        outputs: list[dict] | None = None,
        source_format: TvmSourceFormat | None = None,
        keep_params_in_input: bool | None = None,
        sanitize_input_names: bool | None = None,
    ) -> None:
        super().__init__(path, framework, algorithm, parameters, entry, inputs, outputs)
        self.source_format = source_format
        self.keep_params_in_input = keep_params_in_input
        self.sanitize_input_names = sanitize_input_names


class ModelValidatorTvmIr(ModelValidatorTvm):
    """ModelValidatorTvmIr validator."""

    source_format: TvmSourceFormat | None = None
    keep_params_in_input: bool | None = None
    sanitize_input_names: bool | None = None
