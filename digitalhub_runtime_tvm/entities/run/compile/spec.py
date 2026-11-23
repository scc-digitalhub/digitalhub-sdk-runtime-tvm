# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

import re
from typing import ClassVar

from pydantic import Field, field_validator, model_validator

from digitalhub_runtime_tvm.entities.run._base.spec import RunSpecTvmRun, normalize_model_path
from digitalhub_runtime_tvm.entities.run.compile.models import TvmOptimization, TvmTuning

_CUDA_ARCH_PATTERN = r"^sm_[0-9]+[a-z]?$"
_CUDA_HOST_TRIPLE_PATTERN = r"^(x86_64|amd64|aarch64|arm64)(-[A-Za-z0-9_+.]+)*-linux-gnu$"
_CUDA_DEVICE_LIMITS = ("max_shared_memory_per_block", "max_threads_per_block", "thread_warp_size")
_LLVM_TARGET_PROPERTIES = {
    "mtriple": {"type": "string"},
    "mcpu": {"type": "string"},
    "mfloat-abi": {"type": "string"},
    "mattr": {"type": "array", "items": {"type": "string"}},
    "num-cores": {"type": "integer", "minimum": 1},
}


class RunSpecTvmRunCompile(RunSpecTvmRun):
    """Tvm compile run specifications."""

    # Flat group options are normalized before Pydantic validates the fields.
    ALLOW_EXTRA_INPUTS: ClassVar[bool] = True
    FLAT_OPTION_FIELDS: ClassVar[set[str]] = set(TvmOptimization.model_fields) | set(TvmTuning.model_fields)

    ir_model_path: str | None = None
    target_architecture: str | None = Field(
        default=None, json_schema_extra={"title": "Target profile", "default": "auto"}
    )
    target: dict | None = Field(
        default=None,
        json_schema_extra={
            "title": "Explicit TVM Target",
            "properties": {
                "kind": {"type": "string", "enum": ["llvm", "cuda"]},
                **_LLVM_TARGET_PROPERTIES,
            },
            "if": {"minProperties": 1},
            "then": {"required": ["kind"]},
            "allOf": [
                {
                    "if": {"properties": {"kind": {"const": "cuda"}}, "required": ["kind"]},
                    "then": {
                        "required": ["arch", "host"],
                        "properties": {
                            "arch": {"type": "string", "pattern": _CUDA_ARCH_PATTERN},
                            **{name: {"type": "integer", "minimum": 1} for name in _CUDA_DEVICE_LIMITS},
                            "host": {
                                "type": "object",
                                "properties": {
                                    "kind": {"type": "string", "const": "llvm"},
                                    **_LLVM_TARGET_PROPERTIES,
                                    "mtriple": {"type": "string", "pattern": _CUDA_HOST_TRIPLE_PATTERN},
                                },
                                "required": ["kind", "mtriple"],
                                "additionalProperties": True,
                            },
                        },
                    },
                }
            ],
            "additionalProperties": True,
        },
    )
    optimization: TvmOptimization | None = None
    tuning: TvmTuning | None = None
    tag: str | None = None
    image: str | None = None

    def __init__(self, **data) -> None:
        data = normalize_model_path(data, "ir_model_path")
        data.pop("so_model", None)
        allowed_fields = set(type(self).model_fields) | type(self).FLAT_OPTION_FIELDS
        allowed_fields.update(field.alias for field in type(self).model_fields.values() if isinstance(field.alias, str))
        unknown_fields = sorted(set(data) - allowed_fields)
        if unknown_fields:
            names = ", ".join(unknown_fields)
            raise TypeError(f"Unexpected spec parameter(s) for {type(self).__name__}: {names}")
        super().__init__(**data)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        schema = handler(core_schema)
        schema.setdefault("allOf", []).extend(
            [
                {
                    "if": {"required": ["target"], "properties": {"target": {"type": "object", "minProperties": 1}}},
                    "then": {"properties": {"target_architecture": {"enum": [None, "auto", "cpu", "llvm"]}}},
                },
                {
                    "if": {
                        "required": ["target", "tuning"],
                        "properties": {
                            "target": {
                                "type": "object",
                                "required": ["kind"],
                                "properties": {"kind": {"const": "cuda"}},
                            },
                            "tuning": {
                                "type": "object",
                                "required": ["tuning_mode"],
                                "properties": {"tuning_mode": {"const": "tune"}},
                            },
                        },
                    },
                    "then": {
                        "properties": {
                            "target": {"required": list(_CUDA_DEVICE_LIMITS)},
                            "tuning": {"properties": {"tuning_enable_cpu_cache_flush": {"enum": [None, False]}}},
                        }
                    },
                },
            ]
        )
        return schema

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
        target = self.target
        if not target:
            return self

        if self.target_architecture not in (None, "auto", "cpu", "llvm"):
            raise ValueError("Use target or target_architecture, not both; leave the profile at auto")
        kind = target.get("kind")
        if kind not in ("llvm", "cuda"):
            raise ValueError("target.kind must be llvm or cuda")
        self._validate_llvm_options(target, "target")
        if kind == "cuda":
            self._validate_cuda_target(target)
        return self

    def _validate_cuda_target(self, target: dict) -> None:
        arch = target.get("arch")
        if not isinstance(arch, str) or re.fullmatch(_CUDA_ARCH_PATTERN, arch) is None:
            raise ValueError("target.arch must be an explicit CUDA architecture such as sm_87")
        host = target.get("host")
        if not isinstance(host, dict) or host.get("kind") != "llvm":
            raise ValueError("target.host must be an LLVM target object with kind=llvm")
        triple = host.get("mtriple")
        if not isinstance(triple, str) or re.fullmatch(_CUDA_HOST_TRIPLE_PATTERN, triple) is None:
            raise ValueError("target.host.mtriple must be an explicit Linux GNU AMD64 or ARM64 triple")
        host = dict(host)
        target["host"] = host
        if "num-cores" in host:
            host["num-cores"] = self._positive_integer(host["num-cores"], "target.host.num-cores")
        self._validate_llvm_options(host, "target.host")
        for name in _CUDA_DEVICE_LIMITS:
            if name in target:
                target[name] = self._positive_integer(target[name], f"target.{name}")

        if self.tuning is None or self.tuning.tuning_mode != "tune":
            return
        if self.tuning.tuning_enable_cpu_cache_flush:
            raise ValueError("tuning_enable_cpu_cache_flush is not supported for CUDA tuning")
        for name in _CUDA_DEVICE_LIMITS:
            if name not in target:
                raise ValueError(f"CUDA tuning requires target.{name} from the real device")

    @staticmethod
    def _positive_integer(value, path: str) -> int:
        # JSON Schema integers include integral JSON numbers such as 32.0.
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError(f"{path} must be an integer greater than or equal to 1")
        return value

    @staticmethod
    def _validate_llvm_options(target: dict, path: str) -> None:
        for name in ("mtriple", "mcpu", "mfloat-abi"):
            if name in target and not isinstance(target[name], str):
                raise ValueError(f"{path}.{name} must be a string")
        if "mattr" in target and (
            not isinstance(target["mattr"], list) or any(not isinstance(value, str) for value in target["mattr"])
        ):
            raise ValueError(f"{path}.mattr must be an array of strings")
        num_cores = target.get("num-cores")
        if "num-cores" in target and (isinstance(num_cores, bool) or not isinstance(num_cores, int) or num_cores < 1):
            raise ValueError(f"{path}.num-cores must be an integer greater than or equal to 1")
