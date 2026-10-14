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
    """
    Create and upload an ONNX model entity.

    Parameters
    ----------
    project : str
        Project name.
    source : SourcesOrListOfSources
        Local ONNX model source path or paths.
    name : str, optional
        Entity name. If omitted, it is inferred from ``source``.
    drop_existing : bool, default=False
        Whether to drop an existing entity with the same name.
    path : str, optional
        Destination path. If omitted, it is generated.
    description : str, optional
        Human-readable entity description.
    labels : list[str], optional
        Entity labels.
    version : str, optional
        Entity version.
    framework : str, optional
        Model framework.
    algorithm : str, optional
        Model algorithm.
    parameters : dict, optional
        Model parameters.
    inputs : list[dict], optional
        Input tensor signatures. Each item can define ``name`` (str),
        ``dtype`` (str), ``shape`` (list[int]), ``scale`` (list[float]),
        ``zero_point`` (list[int]), and ``quantized_dimension`` (int).
    outputs : list[dict], optional
        Output tensor signatures, with the same fields as ``inputs``.
    opset : int, optional
        ONNX operator-set version.
    **kwargs : dict
        Additional model specification parameters.

    Returns
    -------
    ModelOnnx
        Created ONNX model entity with uploaded files.
    """
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
    """
    Register an ONNX model entity for an existing source.

    Parameters
    ----------
    project : str
        Project name.
    source : SourcesOrListOfSources
        Path or URI of the existing ONNX model.
    name : str, optional
        Entity name. If omitted, it is inferred from ``source``.
    uuid : str, optional
        Entity identifier.
    version : str, optional
        Entity version.
    description : str, optional
        Human-readable entity description.
    labels : list[str], optional
        Entity labels.
    embedded : bool, default=False
        Whether to embed the entity specification in the project specification.
    extensions : list[dict], optional
        Entity extensions.
    framework : str, optional
        Model framework.
    algorithm : str, optional
        Model algorithm.
    parameters : dict, optional
        Model parameters.
    inputs : list[dict], optional
        Input tensor signatures. Each item can define ``name`` (str),
        ``dtype`` (str), ``shape`` (list[int]), ``scale`` (list[float]),
        ``zero_point`` (list[int]), and ``quantized_dimension`` (int).
    outputs : list[dict], optional
        Output tensor signatures, with the same fields as ``inputs``.
    opset : int, optional
        ONNX operator-set version.
    **kwargs : dict
        Additional model specification parameters.

    Returns
    -------
    ModelOnnx
        Registered ONNX model entity.
    """
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
