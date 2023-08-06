# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

# pylint: disable=protected-access

import copy
import types
from pathlib import Path

from mldesigner import Output as MldesignerOutput
from mldesigner._component import _copy_func
from mldesigner._component_executor import ExecutorBase
from mldesigner._component_generator import MldesignerCommandLineArgument
from mldesigner._constants import (
    BASE_PATH_CONTEXT_KEY,
    IMPORT_AZURE_AI_ML_ERROR_MSG,
    ComponentSource,
    DefaultEnv,
    NodeType,
)
from mldesigner._exceptions import (
    ComponentDefiningError,
    ComponentException,
    ComponentExecutorDependencyException,
    ImportException,
    UserErrorException,
)
from mldesigner._utils import _mldesigner_component_execution

try:
    from azure.ai.ml import (
        Input,
        MpiDistribution,
        Output,
        PyTorchDistribution,
        TensorFlowDistribution,
        load_environment,
    )
    from azure.ai.ml.entities import CommandComponent, Environment, ResourceConfiguration

except ImportError:
    raise ImportException(IMPORT_AZURE_AI_ML_ERROR_MSG)


class DependentComponentExecutor(ExecutorBase):
    """An executor to analyze the entity args of a function and convert it to a runnable component in AzureML."""

    SUPPORTED_RETURN_TYPES = (Output, MldesignerOutput)

    def __init__(self, func: types.FunctionType, entity_args=None, _entry_file=None):
        """Initialize a ComponentExecutor with a function to enable calling the function with command line args.

        :param func: A function wrapped by mldesigner.command_component.
        :type func: types.FunctionType
        """

        if isinstance(func, types.FunctionType):
            arg_mapping = self._analyze_annotations(func)
        else:
            arg_mapping = {}
        super().__init__(func=func, entity_args=entity_args, _entry_file=_entry_file, arg_mapping=arg_mapping)
        self._args_description = self._parse_args_description(func.__doc__)

    @property
    def component(self):
        """
        Return the module entity instance of the component.

        Initialized by the function annotations and the meta data.
        """
        io_properties = self._generate_entity_io_properties(self._arg_mapping)
        command, args = self._entity_args["command"], io_properties.pop("args")
        # for normal command component
        entity_args = copy.copy(self._entity_args)
        entity_args["command"] = self._get_command_str_by_command_args(command, args)
        # Compatibility handling
        try:
            # package version: azure.ai.ml > 0.1.0b4
            from azure.ai.ml.entities._component.component_factory import component_factory

            component = component_factory.load_from_dict(
                _type=NodeType.COMMAND,
                data={**entity_args, **io_properties},
                context={BASE_PATH_CONTEXT_KEY: Path("./")},
                _source=ComponentSource.MLDESIGNER,
            )
            return component
        except ImportError:
            # pylint: disable=no-member
            # package version: azure.ai.ml <= 0.1.0b4
            component = CommandComponent._load_from_dict(
                {**entity_args, **io_properties},
                context={BASE_PATH_CONTEXT_KEY: Path("./")},
                _source=ComponentSource.MLDESIGNER,
            )
            return component
        except Exception as e:
            raise e

    @classmethod
    def _get_command_str_by_command_args(cls, command, args):
        return " ".join(command + args)

    @property
    def _component_dict(self):
        """Return the component entity data as a python dict."""
        return self.component._to_dict()

    def _refresh_instance(self, func):
        self.__init__(self._func, entity_args=self._raw_entity_args, _entry_file=self._entry_file)

    def _update_io_descriptions(self, io):
        for key, val in io.items():
            if not hasattr(val, "description") or not val["description"]:
                if key in self._args_description:
                    val["description"] = self._args_description[key]
        return io

    @classmethod
    def _generate_entity_outputs(cls, arg_mapping) -> dict:
        """Generate output ports of a component, from the return annotation and the arg annotations.

        The outputs including the return values and the special PathOutputPort in args.
        """
        return {val.name: val for val in arg_mapping.values() if isinstance(val, Output)}

    @classmethod
    def _generate_entity_inputs(cls, arg_mapping) -> dict:
        """Generate input ports of the component according to the analyzed argument mapping."""
        return {val.name: val for val in arg_mapping.values() if isinstance(val, Input)}

    def _generate_entity_io_properties(self, arg_mapping):
        """Generate the required properties for a component entity according to the annotation of a function."""
        inputs = self._update_io_descriptions(self._generate_entity_inputs(arg_mapping))
        outputs = self._update_io_descriptions(self._generate_entity_outputs(arg_mapping))
        args = ["--inputs"]
        args += [MldesignerCommandLineArgument(val).arg_group_str() for val in list(inputs.values())]
        args.append("--outputs")
        args += [MldesignerCommandLineArgument(val).arg_group_str() for val in list(outputs.values())]

        return {
            "inputs": {k: v._to_dict() for k, v in inputs.items()},
            "outputs": {k: v._to_dict() for k, v in outputs.items()},
            "args": args,
        }

    @classmethod
    def _analyze_annotations(cls, func):
        """Analyze the annotation of the function to get the parameter mapping dict and the output port list.

        :param func: A function wrapped by mldesigner.command_component.
        :return: (param_mapping, output_list)
            param_mapping: The mapping from function param names to input ports/component parameters;
            output_list: The output port list analyzed from return annotations.
        """
        # Update mldesigner annotation to entity annotation
        f = _update_to_azure_ai_ml_io(func)

        # Compatibility handling
        # package version: azure.ai.ml > 0.1.0b3
        if hasattr(Input, "_get_param_with_standard_annotation") is True:
            return Input._get_param_with_standard_annotation(f)

        try:
            # package version: azure.ai.ml <= 0.1.0b3
            from azure.ai.ml.entities._inputs_outputs import _get_param_with_standard_annotation

            return _get_param_with_standard_annotation(f, is_func=True)
        except ImportError:
            msg = (
                f"{cls.__name__} failed to parse function annotations, "
                f"mldesigner version cannot match any compatible azure-ai-ml package version."
            )
            raise ComponentExecutorDependencyException(msg)

    @classmethod
    def _parse_args_description(cls, docstring):
        """Parse the function docstring and return description for Input/Output

        :param docstring: docstring in func
        :type docstring: str
        :return: A dict mapping for Input/Output and its description
        """
        if hasattr(CommandComponent, "_parse_args_description_from_docstring") is True:
            return CommandComponent._parse_args_description_from_docstring(docstring)

        msg = (
            f"{cls.__name__} failed to parse args description from function docstring, "
            f"mldesigner version cannot match any compatible azure-ai-ml package version."
        )
        raise ComponentExecutorDependencyException(msg)

    @classmethod
    def _get_generate_component_function(cls, component):
        """Return a component generate function according to a component entity"""
        from azure.ai.ml.entities._job.pipeline._load_component import _generate_component_function

        return _generate_component_function(component)

    @classmethod
    def _refine_entity_args(cls, entity_args: dict, return_annotation: dict) -> dict:
        # Deep copy because inner dict may be changed (environment or distribution).
        entity_args = copy.deepcopy(entity_args)
        tags = entity_args.get("tags", {})

        # Convert the type to support old style list tags.
        if isinstance(tags, list):
            tags = {tag: None for tag in tags}

        if not isinstance(tags, dict):
            raise ComponentDefiningError("Keyword 'tags' must be a dict.")

        tags["codegenBy"] = "mldesigner"
        entity_args["tags"] = tags

        if "type" in entity_args and entity_args["type"] == "SweepComponent":
            return entity_args

        core_env = entity_args.get("environment", Environment(image=DefaultEnv.IMAGE, conda_file=DefaultEnv.CONDA_FILE))
        if isinstance(core_env, Environment):
            core_env = core_env._to_dict()
        core_env = cls._update_environment(core_env, return_annotation)
        entity_args["environment"] = core_env

        distribution = entity_args.get("distribution", None)
        if distribution:
            if isinstance(distribution, (PyTorchDistribution, MpiDistribution, TensorFlowDistribution)):
                # Currently there is no entity class for PyTorch/Mpi/Tensorflow, need to change key name to type
                entity_args["distribution"] = copy.deepcopy(distribution.__dict__)

        resources = entity_args.get("resources", None)
        if resources:
            if isinstance(resources, ResourceConfiguration):
                entity_args["resources"] = resources._to_rest_object().as_dict()

        return entity_args

    @classmethod
    def _refine_environment(cls, environment, mldesigner_component_source_dir):
        if cls._is_arm_versioned_str(environment):
            return environment
        environment = (
            Environment(image=DefaultEnv.IMAGE, conda_file=DefaultEnv.CONDA_FILE)
            if _mldesigner_component_execution()
            else cls._refine_environment_to_obj(environment, mldesigner_component_source_dir)
        )
        return environment

    @classmethod
    def _refine_environment_to_obj(cls, environment, mldesigner_component_source_dir) -> Environment:
        if isinstance(environment, dict):
            environment = Environment(**environment)
        if isinstance(environment, (str, Path)):
            environment = Path(mldesigner_component_source_dir) / environment
            environment = load_environment(environment)
        if environment and not isinstance(environment, Environment):
            raise UserErrorException(
                f"Unexpected environment type {type(environment).__name__!r}, "
                f"expected str, path, dict or azure.ai.ml.core.Environment object."
            )
        return environment

    @classmethod
    def _is_arm_versioned_str(cls, env):
        return isinstance(env, str) and env.lower().startswith("azureml:")

    @classmethod
    def _get_outputs_from_return_annotation(cls, func):
        result = super(DependentComponentExecutor, cls)._get_outputs_from_return_annotation(func)
        for k, return_annotation in result.items():
            # normalize to core output
            if isinstance(return_annotation, MldesignerOutput):
                return_annotation = Output(**return_annotation._to_io_entity_args_dict())
            return_annotation.name = k
            result[k] = return_annotation
        return result


def _update_to_azure_ai_ml_io(func) -> dict:
    """This function will translate IOBase from mldesigner package to azure.ai.ml.Input/Output.

    This function depend on `mldesigner._input_output._IOBase._to_io_entity_args_dict` to translate Input/Output
    instance annotations to IO entities.
    This function depend on class names of `mldesigner._input_output` to translate Input/Output class annotations
    to IO entities.
    """
    mldesigner_pkg = "mldesigner"
    annotations = getattr(func, "__annotations__", {})

    def _is_input_or_output_type(io: type, type_str: str):
        """Return true if type name contains type_str"""
        if isinstance(io, type) and io.__module__.startswith(mldesigner_pkg):
            if type_str in io.__name__:
                return True
        return False

    result = {}
    for key, io in annotations.items():
        if isinstance(io, type):
            if _is_input_or_output_type(io, "Input"):
                # mldesigner.Input -> entities.Input
                io = Input
            elif _is_input_or_output_type(io, "Output"):
                # mldesigner.Output -> entities.Output
                io = Output
        elif hasattr(io, "_to_io_entity_args_dict"):
            try:
                if _is_input_or_output_type(type(io), "Input"):
                    # mldesigner.Input() -> entities.Input()
                    io = Input(**io._to_io_entity_args_dict())
                elif _is_input_or_output_type(type(io), "Output"):
                    # mldesigner.Output() -> entities.Output()
                    io = Output(**io._to_io_entity_args_dict())
            except BaseException as e:
                msg = f"Failed to parse {io} to azure-ai-ml Input/Output: {str(e)}"
                raise ComponentException(message=msg) from e
        result[key] = io
    # Copy a new func to set the updated annotation.
    f = _copy_func(func)
    setattr(f, "__annotations__", result)
    return f
