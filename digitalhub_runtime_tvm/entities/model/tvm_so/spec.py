# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub_runtime_tvm.entities.model.tvm.spec import ModelSpecTvm


class ModelSpecTvmSo(ModelSpecTvm):
    """ModelSpecTvmSo specifications."""

    target: str | None = None
    opt_level: int | None = None
    manifest: dict | None = None


class ModelValidatorTvmSo(ModelSpecTvmSo):
    """Compatibility name for the typed TVM shared-object model spec."""
