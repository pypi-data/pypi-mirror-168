# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

__path__ = __import__("pkgutil").extend_path(__path__, __name__)  # type: ignore

from ._component import command_component
from ._execute._execute import execute
from ._generate import generate
from ._input_output import Input, Output
from ._reference_component import reference_component
from ._utils import check_main_package as _check_azure_ai_ml_package

__all__ = ["command_component", "Input", "Output", "reference_component", "generate", "execute"]


_check_azure_ai_ml_package()
