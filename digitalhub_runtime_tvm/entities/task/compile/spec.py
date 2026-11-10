# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from typing import Literal

from digitalhub.entities.task._base.spec import TaskSpecFunction, TaskValidatorFunction
from pydantic import Field


class TaskSpecTvmCompile(TaskSpecFunction):
    """Common task settings and TVM compile options."""

    def __init__(
        self,
        function: str,
        volumes: list[dict] | None = None,
        resources: dict | None = None,
        envs: list[dict] | None = None,
        secrets: list[str] | None = None,
        profile: str | None = None,
        model_path: str | None = None,
        target_architecture: str | None = None,
        target_num_cores: int | None = None,
        opt_level: int | None = None,
        cross_cc: str | None = None,
        exec_mode: Literal["bytecode", "compiled"] | None = None,
        relax_pipeline: str | None = None,
        tir_pipeline: str | None = None,
        system_lib: bool | None = None,
        benchmark_runs: int | None = None,
        params_path: str | None = None,
        tag: str | None = None,
        image: str | None = None,
        tuning_mode: Literal["off", "tune", "apply"] | None = None,
        tuning_trials: int | None = None,
        max_trials_per_task: int | None = None,
        tuning_trials_per_iter: int | None = None,
        tuning_ops: list[str] | None = None,
        tuning_model_path: str | None = None,
        tuning_runner: Literal["local", "rpc"] | None = None,
        tuning_workers: int | None = None,
        tuning_seed: int | None = None,
        tuning_number: int | None = None,
        tuning_repeat: int | None = None,
        tuning_min_repeat_ms: int | None = None,
        tuning_alloc_repeat: int | None = None,
        tuning_enable_cpu_cache_flush: bool | None = None,
        tuning_builder_timeout_sec: float | None = None,
        tuning_runner_timeout_sec: float | None = None,
        rpc_tracker_host: str | None = None,
        rpc_tracker_port: int | None = None,
        rpc_tracker_key: str | None = None,
        rpc_session_timeout_sec: int | None = None,
        allow_partial_tuning: bool | None = None,
    ) -> None:
        super().__init__(
            function=function,
            volumes=volumes,
            resources=resources,
            envs=envs,
            secrets=secrets,
            profile=profile,
        )
        self.model_path = model_path
        self.target_architecture = target_architecture
        self.target_num_cores = target_num_cores
        self.opt_level = opt_level
        self.cross_cc = cross_cc
        self.exec_mode = exec_mode
        self.relax_pipeline = relax_pipeline
        self.tir_pipeline = tir_pipeline
        self.system_lib = system_lib
        self.benchmark_runs = benchmark_runs
        self.params_path = params_path
        self.tag = tag
        self.image = image
        self.tuning_mode = tuning_mode
        self.tuning_trials = tuning_trials
        self.max_trials_per_task = max_trials_per_task
        self.tuning_trials_per_iter = tuning_trials_per_iter
        self.tuning_ops = tuning_ops
        self.tuning_model_path = tuning_model_path
        self.tuning_runner = tuning_runner
        self.tuning_workers = tuning_workers
        self.tuning_seed = tuning_seed
        self.tuning_number = tuning_number
        self.tuning_repeat = tuning_repeat
        self.tuning_min_repeat_ms = tuning_min_repeat_ms
        self.tuning_alloc_repeat = tuning_alloc_repeat
        self.tuning_enable_cpu_cache_flush = tuning_enable_cpu_cache_flush
        self.tuning_builder_timeout_sec = tuning_builder_timeout_sec
        self.tuning_runner_timeout_sec = tuning_runner_timeout_sec
        self.rpc_tracker_host = rpc_tracker_host
        self.rpc_tracker_port = rpc_tracker_port
        self.rpc_tracker_key = rpc_tracker_key
        self.rpc_session_timeout_sec = rpc_session_timeout_sec
        self.allow_partial_tuning = allow_partial_tuning


class TaskValidatorTvmCompile(TaskValidatorFunction):
    """Tvm compile task validator."""

    model_path: str | None = None
    target_architecture: str | None = Field(default=None, json_schema_extra={"default": "auto"})
    target_num_cores: int | None = Field(default=None, ge=1)
    opt_level: int | None = Field(default=None, ge=0, le=3, json_schema_extra={"default": 3})
    cross_cc: str | None = None
    exec_mode: Literal["bytecode", "compiled"] | None = Field(
        default=None, json_schema_extra={"default": "bytecode"}
    )
    relax_pipeline: str | None = Field(default=None, json_schema_extra={"default": "default"})
    tir_pipeline: str | None = Field(default=None, json_schema_extra={"default": "default"})
    system_lib: bool | None = Field(default=None, json_schema_extra={"default": False})
    benchmark_runs: int | None = Field(default=None, ge=0, json_schema_extra={"default": 10})
    params_path: str | None = None
    tag: str | None = None
    image: str | None = None
    tuning_mode: Literal["off", "tune", "apply"] | None = Field(
        default=None, json_schema_extra={"default": "off"}
    )
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
