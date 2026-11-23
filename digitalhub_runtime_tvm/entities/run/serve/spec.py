# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub.entities.task._base.models import CoreServiceType
from pydantic import Field, model_validator

from digitalhub_runtime_tvm.entities.run._base.spec import RunSpecTvmRun, normalize_model_path


class RunSpecTvmRunServe(RunSpecTvmRun):
    """
    Tvm serve run specifications.
    """

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

    @model_validator(mode="before")
    @classmethod
    def read_legacy_path(cls, data):
        return normalize_model_path(data, "so_model_path") if isinstance(data, dict) else data


RunValidatorTvmRunServe = RunSpecTvmRunServe
