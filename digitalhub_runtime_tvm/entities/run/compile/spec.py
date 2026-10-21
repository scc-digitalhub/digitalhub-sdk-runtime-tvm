# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from pydantic import field_validator, model_validator

from digitalhub_runtime_tvm.entities.run._base.spec import RunSpecTvmRun, RunValidatorTvmRun
from digitalhub_runtime_tvm.entities.run.compile.models import TvmOptimization, TvmTuning


class RunSpecTvmRunCompile(RunSpecTvmRun):
    """Tvm compile run specifications."""

    def __init__(
        self,
        task: str,
        model_path: str | None = None,
        target_architecture: str | None = None,
        target: dict | None = None,
        optimization: dict | None = None,
        tuning: dict | None = None,
        tag: str | None = None,
        image: str | None = None,
        **kwargs,
    ) -> None:
        data = RunValidatorTvmRunCompile(
            task=task,
            model_path=model_path,
            target_architecture=target_architecture,
            target=target,
            optimization=optimization,
            tuning=tuning,
            tag=tag,
            image=image,
            **kwargs,
        ).to_dict()
        super().__init__(**data)
        self.model_path = data.get("model_path")
        self.target_architecture = data.get("target_architecture")
        self.target = data.get("target")
        self.optimization = data.get("optimization")
        self.tuning = data.get("tuning")
        self.tag = data.get("tag")
        self.image = data.get("image")


class RunValidatorTvmRunCompile(RunValidatorTvmRun):
    """Tvm compile run validator."""

    model_path: str | None = None
    target_architecture: str | None = None
    target: dict | None = None
    optimization: TvmOptimization | None = None
    tuning: TvmTuning | None = None
    tag: str | None = None
    image: str | None = None

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
            if self.target_architecture not in (None, "auto", "cpu", "llvm"):
                raise ValueError("Use target or target_architecture, not both; leave the profile at auto")
            if self.target.get("kind") != "llvm":
                raise ValueError("target.kind must be llvm; only Linux CPU compilation is supported")
        return self
