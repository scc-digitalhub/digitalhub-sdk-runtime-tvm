# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, model_serializer, model_validator


class _TvmOptions(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    def to_dict(self) -> dict:
        return self.model_dump(by_alias=True, exclude_none=True)


class TvmOptimization(_TvmOptions):
    """Compilation options; omitted values use CORE defaults."""

    target_num_cores: int | None = Field(default=None, ge=1)
    opt_level: int | None = Field(default=None, ge=0, le=3, json_schema_extra={"default": 3})
    cross_cc: str | None = None
    cross_cc_options: list[str] | None = None
    exec_mode: Literal["bytecode", "compiled"] | None = Field(default=None, json_schema_extra={"default": "bytecode"})
    relax_pipeline: str | None = Field(default=None, json_schema_extra={"default": "default"})
    tir_pipeline: str | None = Field(default=None, json_schema_extra={"default": "default"})
    system_lib: bool | None = Field(default=None, json_schema_extra={"default": False})
    benchmark_runs: int | None = Field(default=None, ge=0, json_schema_extra={"default": 10})
    params_path: str | None = None


class TvmTuning(_TvmOptions):
    """MetaSchedule options, validated only while active."""

    _inactive: dict = PrivateAttr(default_factory=dict)

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

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        schema = handler(core_schema)
        fields = schema["properties"]
        apply_names = {"tuning_model_path", "tuning_ops", "allow_partial_tuning"}
        rpc_names = {name for name in fields if name.startswith("rpc_")}
        tune = {
            "properties": {
                name: value
                for name, value in fields.items()
                if name not in rpc_names | {"tuning_mode", "tuning_runner_timeout_sec"}
            },
            "required": ["tuning_trials"],
        }
        tune["properties"]["tuning_trials"] = {"type": "integer", "minimum": 1}
        rpc = {
            "properties": {name: fields[name] for name in rpc_names},
            "required": ["rpc_tracker_host", "rpc_tracker_port", "rpc_tracker_key"],
        }
        for name in ("rpc_tracker_host", "rpc_tracker_key"):
            rpc["properties"][name] = {"type": "string", "pattern": r"\S"}
        rpc["properties"]["rpc_tracker_port"] = {"type": "integer", "minimum": 1, "maximum": 65535}
        tune.update(
            {
                "if": {"required": ["tuning_runner"], "properties": {"tuning_runner": {"const": "rpc"}}},
                "then": rpc,
                "else": {"properties": {"tuning_runner_timeout_sec": fields["tuning_runner_timeout_sec"]}},
            }
        )
        apply = {"properties": {name: fields[name] for name in apply_names}, "required": ["tuning_model_path"]}
        apply["properties"]["tuning_model_path"] = {"type": "string", "pattern": r"\S"}
        schema["properties"] = {name: value if name == "tuning_mode" else {} for name, value in fields.items()}
        schema["allOf"] = [
            {"if": {"required": ["tuning_mode"], "properties": {"tuning_mode": {"const": mode}}}, "then": branch}
            for mode, branch in (("tune", tune), ("apply", apply))
        ]
        return schema

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
