# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.model._base.spec import ModelSpec, ModelValidator

from digitalhub_runtime_tvm.entities.model.tvm.models import TensorSpec


class ModelSpecTflite(ModelSpec):
    """ModelSpecTflite specifications."""

    def __init__(
        self,
        path: str,
        framework: str | None = None,
        algorithm: str | None = None,
        parameters: dict | None = None,
        inputs: list[dict] | None = None,
        outputs: list[dict] | None = None,
    ) -> None:
        super().__init__(path, framework, algorithm, parameters)
        self.inputs = inputs
        self.outputs = outputs


class ModelValidatorTflite(ModelValidator):
    """ModelValidatorTflite validator."""

    inputs: list[TensorSpec] | None = None
    outputs: list[TensorSpec] | None = None
