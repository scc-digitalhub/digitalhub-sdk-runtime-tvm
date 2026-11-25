# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub.plugins import RunSpecFunction
from pydantic import Field, field_validator, model_validator

from digitalhub_runtime_tvm.entities._commons.models import TvmFormat


def normalize_model_path(data: dict, field: str) -> dict:
    if "model_path" not in data:
        return data
    normalized = dict(data)
    previous = normalized.pop("model_path")
    if field in normalized and normalized[field] != previous:
        raise ValueError(f"Conflicting values for model_path and {field}")
    normalized[field] = previous
    return normalized


class RunSpecTvmRun(RunSpecFunction):
    """
    Tvm run specifications.
    """

    model: str | None = None
    inputs: dict[str, str] = Field(default_factory=dict)
    format: TvmFormat | None = Field(default=None, json_schema_extra={"default": "auto"})
    ir_model: str | None = None

    @classmethod
    def from_dict(cls, obj: dict):
        # Older CORE responses include this flag for remote-only runtimes.
        data = dict(obj)
        if data.pop("local_execution", None) not in (None, False):
            raise ValueError("TVM runs support only remote execution")
        return super().from_dict(data)

    @model_validator(mode="before")
    @classmethod
    def ignore_legacy_compiled_model(cls, data):
        if isinstance(data, dict) and "so_model" in data:
            data = {key: value for key, value in data.items() if key != "so_model"}
        return data

    @field_validator("inputs", mode="before")
    @classmethod
    def default_inputs(cls, value):
        return {} if value is None else value
