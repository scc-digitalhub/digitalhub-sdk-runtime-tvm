# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub_runtime_tvm.entities.model.tvm.spec import ModelSpecTvm, ModelValidatorTvm


class ModelSpecTvmSo(ModelSpecTvm):
    """ModelSpecTvmSo specifications."""

    def __init__(
        self,
        path: str,
        framework: str | None = None,
        algorithm: str | None = None,
        parameters: dict | None = None,
        entry: str | None = None,
        inputs: list[dict] | None = None,
        outputs: list[dict] | None = None,
        target: str | None = None,
        opt_level: int | None = None,
        manifest: dict | None = None,
    ) -> None:
        super().__init__(path, framework, algorithm, parameters, entry, inputs, outputs)
        self.target = target
        self.opt_level = opt_level
        self.manifest = manifest


class ModelValidatorTvmSo(ModelValidatorTvm):
    """ModelValidatorTvmSo validator."""

    target: str | None = None
    opt_level: int | None = None
    manifest: dict | None = None
