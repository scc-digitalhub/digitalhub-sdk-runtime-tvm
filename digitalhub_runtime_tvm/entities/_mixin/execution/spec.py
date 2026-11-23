# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub.entities._base.entity.spec import Spec
from digitalhub.entities._frameworks.k8s.models import CoreServiceType
from pydantic import Field


class TvmBuildSpecMixin(Spec):
    """Options for a TVM Build Run."""

    image: str | None = None
    simplify: bool | None = None
    target_opset: int | None = None
    opset_override: int | None = None
    strict_shape_inference: bool | None = None
    data_prop: bool | None = None
    keep_params_in_input: bool | None = None
    sanitize_input_names: bool | None = None
    sort_onnx: bool | None = None


class TvmServeSpecMixin(Spec):
    """Options for a TVM Serve Run."""

    # The shared SDK builder also accepts the field alias in keyword arguments.
    so_model_path: str = Field(
        alias="model_path",
        validation_alias="so_model_path",
        serialization_alias="so_model_path",
        pattern=r"^store://[^/]+/model/tvm-so/[^/:]+:[^/]+$",
    )
    served_name: str | None = Field(default=None, pattern=r"^[a-zA-Z0-9]([a-zA-Z0-9._-]*[a-zA-Z0-9])?$")
    image: str | None = None
    replicas: int | None = Field(default=None, ge=0)
    workers: int | None = Field(default=None, ge=1)
    service_type: CoreServiceType | None = Field(default=None, json_schema_extra={"default": "ClusterIP"})
    service_name: str | None = None
