# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub.entities.task._base.models import CoreServiceType
from digitalhub.entities.task._base.spec import ServeSpecMixin, TaskSpecFunction
from pydantic import Field


class TvmServeSpecMixin(ServeSpecMixin):
    model_path: str | None = Field(default=None, pattern=r"^(store://[^/]+/model/[^/]+/[^:]+(:.+)?)?$")
    served_name: str | None = Field(default=None, pattern=r"^[a-zA-Z0-9]([a-zA-Z0-9._-]*[a-zA-Z0-9])?$")
    image: str | None = None
    workers: int | None = Field(default=None, ge=1)
    service_type: CoreServiceType | None = Field(default=None, json_schema_extra={"default": "ClusterIP"})


class TaskSpecTvmServe(TaskSpecFunction, TvmServeSpecMixin):
    """Common task settings and TVM serve options."""


TaskValidatorTvmServe = TaskSpecTvmServe
