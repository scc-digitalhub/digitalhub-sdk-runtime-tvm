# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub.entities.task._base.models import CoreServiceType
from pydantic import Field

from digitalhub_runtime_tvm.entities.run._base.spec import RunSpecTvmRun


class RunSpecTvmRunServe(RunSpecTvmRun):
    """
    Tvm serve run specifications.
    """

    model_path: str | None = Field(default=None, pattern=r"^(store://[^/]+/model/[^/]+/[^:]+(:.+)?)?$")
    served_name: str | None = Field(default=None, pattern=r"^[a-zA-Z0-9]([a-zA-Z0-9._-]*[a-zA-Z0-9])?$")
    image: str | None = None
    replicas: int | None = Field(default=None, ge=0)
    workers: int | None = Field(default=None, ge=1)
    service_type: CoreServiceType | None = Field(default=None, json_schema_extra={"default": "ClusterIP"})
    service_name: str | None = None


class RunValidatorTvmRunServe(RunSpecTvmRunServe):
    """Compatibility name for the typed TVM serve-run spec."""
