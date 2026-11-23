# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities._base.entity.spec import Spec
from digitalhub.entities._frameworks.k8s.models import CoreServiceType
from digitalhub.entities._mixin.execution.spec import ServeSpecMixin
from pydantic import Field


class TvmBuildSpecMixin(Spec):
    """Build fields shared by TVM tasks and runs."""

    image: str | None = None
    simplify: bool | None = None
    target_opset: int | None = None
    opset_override: int | None = None
    strict_shape_inference: bool | None = None
    data_prop: bool | None = None
    keep_params_in_input: bool | None = None
    sanitize_input_names: bool | None = None


class TvmServeSpecMixin(ServeSpecMixin):
    """Serve fields shared by TVM tasks and runs."""

    model_path: str | None = Field(default=None, pattern=r"^(store://[^/]+/model/[^/]+/[^:]+(:.+)?)?$")
    served_name: str | None = Field(default=None, pattern=r"^[a-zA-Z0-9]([a-zA-Z0-9._-]*[a-zA-Z0-9])?$")
    image: str | None = None
    workers: int | None = Field(default=None, ge=1)
    service_type: CoreServiceType | None = Field(default=None, json_schema_extra={"default": "ClusterIP"})
