# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.entities.model._base.crud import log_base_model, register_base_model
from digitalhub.utils.types import SourcesOrListOfSources

from digitalhub_runtime_tvm.entities._commons.enums import EntityKinds

if typing.TYPE_CHECKING:
    from digitalhub_runtime_tvm.entities.model.tvm_so.entity import ModelTvmSo


def log_tvm_so(
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
    entry: str | None = None,
    inputs: list[dict] | None = None,
    outputs: list[dict] | None = None,
    target: str | None = None,
    opt_level: int | None = None,
    manifest: dict | None = None,
    **kwargs,
) -> ModelTvmSo:
    """
    Create and upload a TVM SO model entity.

    Parameters
    ----------
    project : str
        Project name.
    source : SourcesOrListOfSources
        Local compiled bundle containing both ``model.so`` and ``metadata.json``.
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
    entry : str, optional
        Compiled model entry function.
    inputs : list[dict], optional
        Input tensor signatures. Each item can define ``name`` (str),
        ``dtype`` (str), ``shape`` (list[int]), ``scale`` (list[float]),
        ``zero_point`` (list[int]), and ``quantized_dimension`` (int).
    outputs : list[dict], optional
        Output tensor signatures, with the same fields as ``inputs``.
    target : str, optional
        TVM hardware target used to compile the shared object.
    opt_level : int, optional
        TVM optimization level, from 0 to 3.
    manifest : dict, optional
        Full parsed ``metadata.json`` produced by the compile Run, including TVM
        version/commit and the effective target. Not ``tuning/manifest.json``.
    **kwargs : dict
        Additional model specification parameters.

    Returns
    -------
    ModelTvmSo
        Created TVM SO model entity with uploaded files.

    Examples
    --------
    Log a compiled TVM shared-object model:

    ```python
    import json
    from pathlib import Path
    import digitalhub as dh

    metadata = json.loads(Path("compiled-model/metadata.json").read_text())
    model = dh.log_tvm_so(
        project="my-project",
        name="resnet18-tvm",
        source="./compiled-model/",
        target=metadata["target"],
        opt_level=metadata["opt_level"],
        entry=metadata["entry"],
        inputs=metadata["inputs"],
        outputs=metadata["outputs"],
        manifest=metadata,
    )
    ```
    """
    return log_base_model(
        project=project,
        name=name,
        kind=EntityKinds.MODEL_TVM_SO.value,
        source=source,
        drop_existing=drop_existing,
        path=path,
        description=description,
        labels=labels,
        version=version,
        framework=framework,
        algorithm=algorithm,
        parameters=parameters,
        entry=entry,
        inputs=inputs,
        outputs=outputs,
        target=target,
        opt_level=opt_level,
        manifest=manifest,
        **kwargs,
    )


def register_tvm_so(
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
    entry: str | None = None,
    inputs: list[dict] | None = None,
    outputs: list[dict] | None = None,
    target: str | None = None,
    opt_level: int | None = None,
    manifest: dict | None = None,
    **kwargs,
) -> ModelTvmSo:
    """
    Register a TVM SO model entity for an existing source.

    Parameters
    ----------
    project : str
        Project name.
    source : SourcesOrListOfSources
        Directory or URI of the existing compiled bundle, including ``metadata.json``.
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
    entry : str, optional
        Compiled model entry function.
    inputs : list[dict], optional
        Input tensor signatures. Each item can define ``name`` (str),
        ``dtype`` (str), ``shape`` (list[int]), ``scale`` (list[float]),
        ``zero_point`` (list[int]), and ``quantized_dimension`` (int).
    outputs : list[dict], optional
        Output tensor signatures, with the same fields as ``inputs``.
    target : str, optional
        TVM hardware target used to compile the shared object.
    opt_level : int, optional
        TVM optimization level, from 0 to 3.
    manifest : dict, optional
        Full parsed ``metadata.json`` produced by the compile Run, including TVM
        version/commit and the effective target. Not ``tuning/manifest.json``.
    **kwargs : dict
        Additional model specification parameters.

    Returns
    -------
    ModelTvmSo
        Registered TVM SO model entity.

    Examples
    --------
    Register an uploaded bundle using a local copy of its metadata:

    ```python
    import json
    from pathlib import Path
    import digitalhub as dh

    metadata = json.loads(Path("compiled-model/metadata.json").read_text())
    model = dh.register_tvm_so(
        project="my-project",
        name="registered-resnet18-tvm",
        source="s3://my-bucket/models/resnet18-so/",
        target=metadata["target"],
        opt_level=metadata["opt_level"],
        entry=metadata["entry"],
        inputs=metadata["inputs"],
        outputs=metadata["outputs"],
        manifest=metadata,
    )
    ```
    """
    return register_base_model(
        project=project,
        source=source,
        entity_kind=EntityKinds.MODEL_TVM_SO.value,
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
        entry=entry,
        inputs=inputs,
        outputs=outputs,
        target=target,
        opt_level=opt_level,
        manifest=manifest,
        **kwargs,
    )
