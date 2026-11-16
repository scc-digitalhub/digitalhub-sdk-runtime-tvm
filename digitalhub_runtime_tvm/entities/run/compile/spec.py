# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from typing import ClassVar

from pydantic import Field, field_validator, model_validator

from digitalhub_runtime_tvm.entities.run._base.spec import RunSpecTvmRun
from digitalhub_runtime_tvm.entities.run.compile.models import TvmOptimization, TvmTuning


class RunSpecTvmRunCompile(RunSpecTvmRun):
    """Tvm compile run specifications."""

    # Flat group options are normalized before Pydantic validates the fields.
    ALLOW_EXTRA_INPUTS: ClassVar[bool] = True
    FLAT_OPTION_FIELDS: ClassVar[set[str]] = set(TvmOptimization.model_fields) | set(TvmTuning.model_fields)

    model_path: str | None = None
    target_architecture: str | None = Field(default=None, json_schema_extra={"default": "auto"})
    target: dict | None = Field(
        default=None,
        json_schema_extra={
            "title": "Explicit TVM Target",
            "properties": {
                "kind": {"type": "string", "pattern": "^llvm$"},
                "mtriple": {"type": "string"},
                "mcpu": {"type": "string"},
                "mfloat-abi": {"type": "string"},
                "mattr": {"type": "array", "items": {"type": "string"}},
                "num-cores": {"type": "integer", "minimum": 1},
            },
            "if": {"minProperties": 1},
            "then": {"required": ["kind"]},
            "additionalProperties": True,
        },
    )
    optimization: TvmOptimization | None = None
    tuning: TvmTuning | None = None
    tag: str | None = None
    image: str | None = None

    def __init__(self, **data) -> None:
        allowed_fields = set(type(self).model_fields) | type(self).FLAT_OPTION_FIELDS
        allowed_fields.update(field.alias for field in type(self).model_fields.values() if isinstance(field.alias, str))
        unknown_fields = sorted(set(data) - allowed_fields)
        if unknown_fields:
            names = ", ".join(unknown_fields)
            raise TypeError(f"Unexpected spec parameter(s) for {type(self).__name__}: {names}")
        super().__init__(**data)

    @model_validator(mode="before")
    @classmethod
    def group_options(cls, value):
        if not isinstance(value, dict):
            return value
        data = dict(value)
        for name, model in (("optimization", TvmOptimization), ("tuning", TvmTuning)):
            flat = {field: data.pop(field) for field in model.model_fields if field in data}
            group = data.pop(name, None)
            if isinstance(group, model):
                group = group.to_dict()
            if group is not None:
                if not isinstance(group, dict):
                    raise ValueError(f"{name} must be an object")
                flat.update(group)
            if flat:
                data[name] = flat
        return data

    @field_validator("target_architecture", mode="before")
    @classmethod
    def normalize_target(cls, value):
        if isinstance(value, str):
            return value.strip().lower() or None
        return value

    @model_validator(mode="after")
    def validate_target(self):
        if self.target:
            if self.target_architecture not in (None, "auto"):
                raise ValueError("Use target or target_architecture, not both; leave the profile at auto")
            if self.target.get("kind") != "llvm":
                raise ValueError("target.kind must be llvm; only Linux CPU compilation is supported")
            for name in ("mtriple", "mcpu", "mfloat-abi"):
                if name in self.target and not isinstance(self.target[name], str):
                    raise ValueError(f"target.{name} must be a string")
            if "mattr" in self.target and (
                not isinstance(self.target["mattr"], list)
                or any(not isinstance(value, str) for value in self.target["mattr"])
            ):
                raise ValueError("target.mattr must be an array of strings")
            num_cores = self.target.get("num-cores")
            if "num-cores" in self.target and (
                isinstance(num_cores, bool) or not isinstance(num_cores, int) or num_cores < 1
            ):
                raise ValueError("target.num-cores must be an integer greater than or equal to 1")
        return self


class RunValidatorTvmRunCompile(RunSpecTvmRunCompile):
    """Compatibility name for the typed TVM compile-run spec."""
