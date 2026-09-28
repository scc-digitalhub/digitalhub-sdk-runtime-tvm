# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.entities.function.crud import new_function

from digitalhub_runtime_tvm.entities.function.tvm.builder import FunctionTvmBuilder
from digitalhub_runtime_tvm.entities.function.tvm.spec import TvmFormat

if typing.TYPE_CHECKING:
    from digitalhub_runtime_tvm.entities.function.tvm.entity import FunctionTvm


def new_function_tvm(
    project: str,
    name: str,
    model: str,
    format: TvmFormat | None = None,
    ir_model: str | None = None,
    so_model: str | None = None,
    uuid: str | None = None,
    version: str | None = None,
    description: str | None = None,
    labels: list[str] | None = None,
    embedded: bool = False,
) -> FunctionTvm:
    """Create a TVM function entity."""
    return new_function(
        project=project,
        name=name,
        kind=FunctionTvmBuilder.ENTITY_KIND,
        uuid=uuid,
        version=version,
        description=description,
        labels=labels,
        embedded=embedded,
        model=model,
        format=format,
        ir_model=ir_model,
        so_model=so_model,
    )
