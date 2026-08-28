# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from typing import Literal

from digitalhub.entities.task._base.spec import TaskSpecFunction, TaskValidatorFunction
from pydantic import Field

TvmTargetArchitecture = Literal["cpu", "llvm", "x86", "arm64", "armv7l"]


class TaskSpecTvmCompile(TaskSpecFunction):
    """
    Tvm compile task specifications.
    """

    def __init__(
        self,
        function: str,
        volumes: list[dict] | None = None,
        resources: dict | None = None,
        envs: list[dict] | None = None,
        secrets: list[str] | None = None,
        profile: str | None = None,
        model_path: str | None = None,
        target_architecture: TvmTargetArchitecture | None = None,
        opt_level: int | None = None,
        cross_cc: str | None = None,
        exec_mode: str | None = None,
        relax_pipeline: str | None = None,
        tir_pipeline: str | None = None,
        system_lib: bool | None = None,
        params_path: str | None = None,
        tag: str | None = None,
        image: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            function=function,
            volumes=volumes,
            resources=resources,
            envs=envs,
            secrets=secrets,
            profile=profile,
            **kwargs,
        )
        self.model_path = model_path
        self.target_architecture = target_architecture
        self.opt_level = opt_level
        self.cross_cc = cross_cc
        self.exec_mode = exec_mode
        self.relax_pipeline = relax_pipeline
        self.tir_pipeline = tir_pipeline
        self.system_lib = system_lib
        self.params_path = params_path
        self.tag = tag
        self.image = image


class TaskValidatorTvmCompile(TaskValidatorFunction):
    """
    Tvm compile task validator.
    """

    model_path: str | None = None
    target_architecture: TvmTargetArchitecture | None = None
    opt_level: int | None = Field(default=None, ge=0)
    cross_cc: str | None = None
    exec_mode: str | None = None
    relax_pipeline: str | None = None
    tir_pipeline: str | None = None
    system_lib: bool | None = None
    params_path: str | None = None
    tag: str | None = None
    image: str | None = None
