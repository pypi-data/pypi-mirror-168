# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from enum import Enum

BASE_PATH_CONTEXT_KEY = "base_path"
VALID_NAME_CHARS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-")
MLDESIGNER_COMPONENT_EXECUTION = "MLDESIGNER_COMPONENT_EXECUTION"
MLDESIGNER_COMPONENT_EXECUTOR_MODULE = "mldesigner.executor"
IMPORT_AZURE_AI_ML_ERROR_MSG = (
    "Dependent component executor can not be used in standalone mode. Please install auzre.ai.ml package."
)
REGISTRY_URI_FORMAT = "azureml://registries/"


class NodeType(object):
    COMMAND = "command"
    SWEEP = "sweep"
    PARALLEL = "parallel"
    AUTOML = "automl"
    PIPELINE = "pipeline"
    IMPORT = "import"
    SPARK = "spark"
    # Note: container is not a real component type,
    # only used to mark component from container data.
    _CONTAINER = "_container"


class DefaultEnv:
    CONDA_FILE = {
        "name": "default_environment",
        "channels": ["defaults"],
        "dependencies": [
            "python=3.8.12",
            "pip=21.2.2",
            {
                "pip": [
                    "--extra-index-url=https://azuremlsdktestpypi.azureedge.net/sdk-cli-v2",
                    "mldesigner==0.0.72212755",
                ]
            },
        ],
    }
    IMAGE = "mcr.microsoft.com/azureml/openmpi3.1.2-ubuntu18.04"


class ComponentSource:
    """Indicate where the component is constructed."""

    MLDESIGNER = "MLDESIGNER"


class IoConstants:
    PRIMITIVE_STR_2_TYPE = {"integer": int, "string": str, "number": float, "boolean": bool}
    PRIMITIVE_TYPE_2_STR = {int: "integer", str: "string", float: "number", bool: "boolean"}
    TYPE_MAPPING_YAML_2_REST = {
        "string": "String",
        "integer": "Integer",
        "number": "Number",
        "boolean": "Boolean",
    }
    PARAM_PARSERS = {
        "float": float,
        "integer": lambda v: int(float(v)),  # backend returns 10.0 for integer, parse it to float before int
        "boolean": lambda v: str(v).lower() == "true",
        "number": float,
    }
    # For validation, indicates specific parameters combination for each type
    INPUT_TYPE_COMBINATION = {
        "uri_folder": ["path", "mode"],
        "uri_file": ["path", "mode"],
        "mltable": ["path", "mode"],
        "mlflow_model": ["path", "mode"],
        "custom_model": ["path", "mode"],
        "integer": ["default", "min", "max"],
        "number": ["default", "min", "max"],
        "string": ["default"],
        "boolean": ["default"],
    }


class AssetTypes:
    URI_FILE = "uri_file"
    URI_FOLDER = "uri_folder"
    MLTABLE = "mltable"
    MLFLOW_MODEL = "mlflow_model"
    TRITON_MODEL = "triton_model"
    CUSTOM_MODEL = "custom_model"


class ErrorCategory:

    USER_ERROR = "UserError"
    SYSTEM_ERROR = "SystemError"
    UNKNOWN = "Unknown"


class SupportedParameterTypes(str, Enum):  # pylint: disable=enum-must-inherit-case-insensitive-enum-meta
    NUMBER = "number"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    STRING = "string"
