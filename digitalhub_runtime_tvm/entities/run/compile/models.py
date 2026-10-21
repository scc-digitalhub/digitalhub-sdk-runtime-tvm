# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from typing import Literal

from digitalhub.entities._base.entity.spec import SpecValidator
from pydantic import ConfigDict, Field, PrivateAttr, model_serializer, model_validator


class TvmOptimization(SpecValidator):
    """Compilation options; omitted values use CORE defaults."""

    model_config = ConfigDict(extra="forbid")

    target_num_cores: int | None = Field(default=None, ge=1)
    opt_level: int | None = Field(default=None, ge=0, le=3)
    cross_cc: str | None = None
    cross_cc_options: list[str] | None = None
    exec_mode: Literal["bytecode", "compiled"] | None = None
    relax_pipeline: str | None = None
    tir_pipeline: str | None = None
    system_lib: bool | None = None
    benchmark_runs: int | None = Field(default=None, ge=0)
    params_path: str | None = None


class TvmTuning(SpecValidator):
    """MetaSchedule options, validated only while active."""

    model_config = ConfigDict(extra="forbid")
    _inactive: dict = PrivateAttr(default_factory=dict)

    tuning_mode: Literal["off", "tune", "apply"] | None = None
    tuning_trials: int | None = Field(default=None, ge=1)
    max_trials_per_task: int | None = Field(default=None, ge=1)
    tuning_trials_per_iter: int | None = Field(default=None, ge=1)
    tuning_ops: list[str] | None = None
    tuning_model_path: str | None = None
    tuning_runner: Literal["local", "rpc"] | None = None
    tuning_workers: int | None = Field(default=None, ge=1)
    tuning_seed: int | None = Field(default=None, ge=0)
    tuning_number: int | None = Field(default=None, ge=1)
    tuning_repeat: int | None = Field(default=None, ge=1)
    tuning_min_repeat_ms: int | None = Field(default=None, ge=0)
    tuning_alloc_repeat: int | None = Field(default=None, ge=1)
    tuning_enable_cpu_cache_flush: bool | None = None
    tuning_builder_timeout_sec: float | None = Field(default=None, gt=0, allow_inf_nan=False)
    tuning_runner_timeout_sec: float | None = Field(default=None, gt=0, allow_inf_nan=False)
    rpc_tracker_host: str | None = None
    rpc_tracker_port: int | None = Field(default=None, ge=1, le=65535)
    rpc_tracker_key: str | None = None
    rpc_session_timeout_sec: int | None = Field(default=None, ge=1)
    allow_partial_tuning: bool | None = None

    @model_validator(mode="wrap")
    @classmethod
    def validate_active_options(cls, value, handler):
        if not isinstance(value, dict):
            return handler(value)

        data = dict(value)
        mode = data.get("tuning_mode") or "off"
        fields = cls.model_fields.keys() - {"tuning_mode"}
        inactive = set()
        if mode == "off":
            inactive = fields
        elif mode == "apply":
            inactive = fields - {"tuning_model_path", "tuning_ops", "allow_partial_tuning"}
        elif mode == "tune":
            runner = data.get("tuning_runner") or "local"
            if runner == "local":
                inactive = {name for name in fields if name.startswith("rpc_")}
            elif runner == "rpc":
                inactive = {"tuning_runner_timeout_sec"}

        preserved = {name: data.pop(name) for name in inactive if name in data}
        result = handler(data)
        result._inactive = preserved
        if mode == "apply" and not (result.tuning_model_path or "").strip():
            raise ValueError("tuning_mode=apply requires tuning_model_path")
        if mode == "tune":
            if result.tuning_trials is None:
                raise ValueError("tuning_mode=tune requires tuning_trials")
            if result.tuning_runner == "rpc" and (
                not (result.rpc_tracker_host or "").strip()
                or result.rpc_tracker_port is None
                or not (result.rpc_tracker_key or "").strip()
            ):
                raise ValueError("tuning_runner=rpc requires rpc_tracker_host, rpc_tracker_port, and rpc_tracker_key")
        return result

    @model_serializer(mode="wrap")
    def serialize_options(self, handler, info):
        data = handler(self)
        data.update({key: value for key, value in self._inactive.items() if value is not None or not info.exclude_none})
        return data
