# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.entities.model._base.crud import log_base_model, register_base_model
from digitalhub.utils.types import SourcesOrListOfSources

from digitalhub_runtime_tvm.entities._commons.enums import EntityKinds

if typing.TYPE_CHECKING:
    from digitalhub_runtime_tvm.entities.model.onnx.entity import ModelOnnx


def log_onnx(
    project: str,
    source: SourcesOrListOfSources,
    name: str | None = None,
    drop_existing: bool = False,
    path: str | None = None,
    description: str | None = None,
    labels: list[str] | None = None,
    version: str | None = None,
    framework: str | None = None,
    algorithm: str | None = None,
    parameters: dict | None = None,
    inputs: list[dict] | None = None,
    outputs: list[dict] | None = None,
    opset: int | None = None,
    **kwargs,
) -> ModelOnnx:
    """Create and upload an ONNX model entity."""
    return log_base_model(
        project=project,
        name=name,
        kind=EntityKinds.MODEL_ONNX.value,
        source=source,
        drop_existing=drop_existing,
        path=path,
        description=description,
        labels=labels,
        version=version,
        framework=framework,
        algorithm=algorithm,
        parameters=parameters,
        inputs=inputs,
        outputs=outputs,
        opset=opset,
        **kwargs,
    )


def register_onnx(
    project: str,
    source: SourcesOrListOfSources,
    name: str | None = None,
    uuid: str | None = None,
    version: str | None = None,
    description: str | None = None,
    labels: list[str] | None = None,
    embedded: bool = False,
    extensions: list[dict] | None = None,
    framework: str | None = None,
    algorithm: str | None = None,
    parameters: dict | None = None,
    inputs: list[dict] | None = None,
    outputs: list[dict] | None = None,
    opset: int | None = None,
    **kwargs,
) -> ModelOnnx:
    """Register an ONNX model entity for an existing source."""
    return register_base_model(
        project=project,
        source=source,
        entity_kind=EntityKinds.MODEL_ONNX.value,
        name=name,
        uuid=uuid,
        version=version,
        description=description,
        labels=labels,
        embedded=embedded,
        extensions=extensions,
        framework=framework,
        algorithm=algorithm,
        parameters=parameters,
        inputs=inputs,
        outputs=outputs,
        opset=opset,
        **kwargs,
    )
