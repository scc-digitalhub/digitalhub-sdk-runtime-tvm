# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub.factory.plugins import CrudPlugin, EntityPlugin

from digitalhub_runtime_tvm.entities.function.tvm.builder import FunctionTvmBuilder
from digitalhub_runtime_tvm.entities.function.tvm.crud import new_function_tvm
from digitalhub_runtime_tvm.entities.model.onnx.builder import ModelOnnxBuilder
from digitalhub_runtime_tvm.entities.model.onnx.crud import log_onnx, register_onnx
from digitalhub_runtime_tvm.entities.model.tflite.builder import ModelTfliteBuilder
from digitalhub_runtime_tvm.entities.model.tflite.crud import log_tflite, register_tflite
from digitalhub_runtime_tvm.entities.model.tvm_ir.builder import ModelTvmIrBuilder
from digitalhub_runtime_tvm.entities.model.tvm_ir.crud import log_tvm_ir, register_tvm_ir
from digitalhub_runtime_tvm.entities.model.tvm_so.builder import ModelTvmSoBuilder
from digitalhub_runtime_tvm.entities.model.tvm_so.crud import log_tvm_so, register_tvm_so
from digitalhub_runtime_tvm.entities.run.build.builder import RunTvmRunBuildBuilder
from digitalhub_runtime_tvm.entities.run.compile.builder import RunTvmRunCompileBuilder
from digitalhub_runtime_tvm.entities.run.serve.builder import RunTvmRunServeBuilder
from digitalhub_runtime_tvm.entities.task.build.builder import TaskTvmBuildBuilder
from digitalhub_runtime_tvm.entities.task.compile.builder import TaskTvmCompileBuilder
from digitalhub_runtime_tvm.entities.task.serve.builder import TaskTvmServeBuilder

function_tvm_plugin = EntityPlugin(
    builder=FunctionTvmBuilder,
    shortcuts=(CrudPlugin(new_function_tvm),),
)
model_onnx_plugin = EntityPlugin(
    builder=ModelOnnxBuilder,
    shortcuts=(CrudPlugin(log_onnx), CrudPlugin(register_onnx)),
)
model_tflite_plugin = EntityPlugin(
    builder=ModelTfliteBuilder,
    shortcuts=(CrudPlugin(log_tflite), CrudPlugin(register_tflite)),
)
model_tvm_ir_plugin = EntityPlugin(
    builder=ModelTvmIrBuilder,
    shortcuts=(CrudPlugin(log_tvm_ir), CrudPlugin(register_tvm_ir)),
)
model_tvm_so_plugin = EntityPlugin(
    builder=ModelTvmSoBuilder,
    shortcuts=(CrudPlugin(log_tvm_so), CrudPlugin(register_tvm_so)),
)

entity_plugins = (
    model_onnx_plugin,
    model_tflite_plugin,
    model_tvm_ir_plugin,
    model_tvm_so_plugin,
    function_tvm_plugin,
    EntityPlugin(builder=TaskTvmBuildBuilder),
    EntityPlugin(builder=TaskTvmCompileBuilder),
    EntityPlugin(builder=TaskTvmServeBuilder),
    EntityPlugin(builder=RunTvmRunBuildBuilder),
    EntityPlugin(builder=RunTvmRunCompileBuilder),
    EntityPlugin(builder=RunTvmRunServeBuilder),
)
