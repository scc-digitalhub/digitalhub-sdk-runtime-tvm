# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from typing import Literal

from digitalhub.entities.task._base.spec import TaskSpecFunction
from pydantic import Field


class TaskSpecTvmCompile(TaskSpecFunction):
    """Common task settings and TVM compile options."""

    model_path: str | None = None
    target_architecture: str | None = Field(default=None, json_schema_extra={"default": "auto"})
    target_num_cores: int | None = Field(default=None, ge=1)
    opt_level: int | None = Field(default=None, ge=0, le=3, json_schema_extra={"default": 3})
    cross_cc: str | None = None
    exec_mode: Literal["bytecode", "compiled"] | None = Field(default=None, json_schema_extra={"default": "bytecode"})
    relax_pipeline: str | None = Field(default=None, json_schema_extra={"default": "default"})
    tir_pipeline: str | None = Field(default=None, json_schema_extra={"default": "default"})
    system_lib: bool | None = Field(default=None, json_schema_extra={"default": False})
    benchmark_runs: int | None = Field(default=None, ge=0, json_schema_extra={"default": 10})
    params_path: str | None = None
    tag: str | None = None
    image: str | None = None
    tuning_mode: Literal["off", "tune", "apply"] | None = Field(default=None, json_schema_extra={"default": "off"})
    tuning_trials: int | None = Field(default=None, ge=1)
    max_trials_per_task: int | None = Field(default=None, ge=1, json_schema_extra={"default": 16})
    tuning_trials_per_iter: int | None = Field(default=None, ge=1, json_schema_extra={"default": 64})
    tuning_ops: list[str] | None = None
    tuning_model_path: str | None = None
    tuning_runner: Literal["local", "rpc"] | None = Field(default=None, json_schema_extra={"default": "local"})
    tuning_workers: int | None = Field(default=None, ge=1)
    tuning_seed: int | None = Field(default=None, ge=0, json_schema_extra={"default": 0})
    tuning_number: int | None = Field(default=None, ge=1, json_schema_extra={"default": 3})
    tuning_repeat: int | None = Field(default=None, ge=1, json_schema_extra={"default": 1})
    tuning_min_repeat_ms: int | None = Field(default=None, ge=0, json_schema_extra={"default": 100})
    tuning_alloc_repeat: int | None = Field(default=None, ge=1, json_schema_extra={"default": 1})
    tuning_enable_cpu_cache_flush: bool | None = Field(default=None, json_schema_extra={"default": False})
    tuning_builder_timeout_sec: float | None = Field(
        default=None, gt=0, allow_inf_nan=False, json_schema_extra={"default": 30}
    )
    tuning_runner_timeout_sec: float | None = Field(
        default=None, gt=0, allow_inf_nan=False, json_schema_extra={"default": 30}
    )
    rpc_tracker_host: str | None = None
    rpc_tracker_port: int | None = Field(default=None, ge=1, le=65535)
    rpc_tracker_key: str | None = None
    rpc_session_timeout_sec: int | None = Field(default=None, ge=1, json_schema_extra={"default": 60})
    allow_partial_tuning: bool | None = Field(default=None, json_schema_extra={"default": False})


TaskValidatorTvmCompile = TaskSpecTvmCompile
