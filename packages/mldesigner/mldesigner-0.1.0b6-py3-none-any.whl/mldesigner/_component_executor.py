# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

# pylint: disable=too-many-instance-attributes, protected-access, unused-argument

import copy
import importlib
import inspect
import json
import sys
import types
from abc import abstractmethod
from pathlib import Path

from mldesigner._constants import AssetTypes, ComponentSource, IoConstants, NodeType, SupportedParameterTypes
from mldesigner._exceptions import (
    ComponentDefiningError,
    ImportException,
    NoComponentError,
    RequiredComponentNameError,
    RequiredParamParsingError,
    TooManyComponentsError,
    UserErrorException,
    ValidationException,
)
from mldesigner._input_output import Input, Output, _standalone_get_param_with_standard_annotation
from mldesigner._logger_factory import _LoggerFactory
from mldesigner._utils import _import_component_with_working_dir, _is_mldesigner_component, inject_sys_path

execute_logger = _LoggerFactory.get_logger("execute", target_stdout=True)


class ExecutorBase:
    """An executor base. Only to be inherited for sub executor classes."""

    INJECTED_FIELD = "_entity_args"  # The injected field is used to get the component spec args of the function.
    CODE_GEN_BY_KEY = "codegenBy"
    SPECIAL_FUNC_CHECKERS = {
        "Coroutine": inspect.iscoroutinefunction,
        "Generator": inspect.isgeneratorfunction,
    }
    # This is only available on Py3.6+
    if sys.version_info.major == 3 and sys.version_info.minor > 5:
        SPECIAL_FUNC_CHECKERS["Async generator"] = inspect.isasyncgenfunction
    DEFAULT_OUTPUT_NAME = "output"
    CONTROL_OUTPUTS_KEY = "azureml.pipeline.control"
    SUPPORTED_RETURN_TYPES = (Output,)

    def __init__(self, func: types.FunctionType, arg_mapping, entity_args=None, _entry_file=None):
        """Initialize a ComponentExecutor with a function to enable calling the function with command line args.

        :param func: A function decorated by mldesigner.command_component.
        :type func: types.FunctionType
        :param arg_mapping: A dict mapping from parameter name to annotation.
        :type arg_mapping: dict
        :param entity_args: Component entity dict.
        :type entity_args: dict
        :param _entry_file: Component entry file path.
        :type _entry_file: str
        """
        if not isinstance(func, types.FunctionType):
            msg = "Only function type is allowed to initialize ComponentExecutor."
            raise ValidationException(message=msg)
        if entity_args is None:
            entity_args = getattr(func, self.INJECTED_FIELD, None)
            if entity_args is None:
                msg = "You must wrap the function with mldesigner component decorators before using it."
                raise ValidationException(message=msg)
        self._raw_entity_args = copy.deepcopy(entity_args)
        self._entity_args = copy.deepcopy(entity_args)
        self._name = entity_args["name"]
        self._type = entity_args.get("type", NodeType.COMMAND)
        self._entity_file_path = None
        self._assert_valid_func(func)
        self._arg_mapping = arg_mapping
        self._return_mapping = self._get_output_annotations(func=func, mapping=self._arg_mapping)
        self._execution_args = None
        self._execution_outputs = None
        self._additional_args = None  # used to notify user for additional args that are useless after execution
        if _is_mldesigner_component(func):
            # If is mldesigner component func, set the func and entry file as original value
            self._func = func._executor._func
            self._entry_file = func._executor._entry_file
        else:
            # Else, set func directly, if _entry_file is None, resolve it from func.
            # Note: The entry file here might not equal with inspect.getfile(component._func),
            # as we can define raw func in file A and wrap it with mldesigner component in file B.
            # For the example below, we set entry file as B here (the mldesigner component defined in).
            self._func = func
            self._entry_file = _entry_file if _entry_file else Path(inspect.getfile(self._func)).absolute()

    def _assert_valid_func(self, func):
        """Check whether the function is valid, if it is not valid, raise."""
        for k, checker in self.SPECIAL_FUNC_CHECKERS.items():
            if checker(func):
                raise NotImplementedError("%s function is not supported for %s now." % (k, self._type))

    def __call__(self, *args, **kwargs):
        """Directly calling a component executor will return the executor copy with processed inputs."""
        # transform *args and **kwargs to a parameter dict
        EXECUTOR_CLASS = self._get_executor_class()
        new_executor = EXECUTOR_CLASS(func=self._func)
        new_executor._execution_args = dict(
            inspect.signature(new_executor._func).bind_partial(*args, **kwargs).arguments
        )
        return new_executor

    @classmethod
    def _collect_component_from_file(
        cls, py_file, working_dir=None, force_reload=False, component_name=None, from_executor=False
    ):
        """Collect single mldesigner component in a file and return the executors of the components."""
        py_file = Path(py_file).absolute()
        if py_file.suffix != ".py":
            msg = "{} is not a valid py file."
            raise ValidationException(message=msg.format(py_file))
        if working_dir is None:
            working_dir = py_file.parent
        working_dir = Path(working_dir).absolute()

        component_path = py_file.relative_to(working_dir).as_posix().split(".")[0].replace("/", ".")

        component = cls._collect_component_from_py_module(
            component_path,
            working_dir=working_dir,
            force_reload=force_reload,
            component_name=component_name,
            from_executor=from_executor,
        )
        if not component and from_executor:
            raise NoComponentError(py_file, component_name)
        return component

    @classmethod
    def _collect_component_from_py_module(
        cls, py_module, working_dir, force_reload=False, component_name=None, from_executor=False
    ):
        """Collect single mldesigner component in a py module and return the executors of the components."""
        components = list(cls._collect_components_from_py_module(py_module, working_dir, force_reload))

        def defined_in_current_file(component):
            # The entry file here might not equal with inspect.getfile(component._func),
            # as we can define raw func in file A and wrap it with mldesigner component in file B.
            # For the example below, we got entry file as B here (the mldesigner component defined in).
            entry_file = component._entry_file
            component_path = py_module.replace(".", "/") + ".py"
            return Path(entry_file).resolve().absolute() == (Path(working_dir) / component_path).resolve().absolute()

        components = [
            component
            for component in components
            if defined_in_current_file(component) and (not component_name or component._name == component_name)
        ]
        if len(components) == 0:
            return None
        component = components[0]
        entry_file = Path(inspect.getfile(component._func))
        if component_name and len(components) > 1:
            if from_executor:
                if not component_name:
                    raise RequiredComponentNameError(entry_file)
                raise TooManyComponentsError(len(components), entry_file, component_name)
            # Calls from pipeline project with no component name.
            raise TooManyComponentsError(len(components), entry_file)
        return component

    @classmethod
    def _collect_components_from_py_module(cls, py_module, working_dir=None, force_reload=False):
        """Collect all components in a python module and return the executors of the components."""
        if isinstance(py_module, str):
            try:
                py_module = _import_component_with_working_dir(py_module, working_dir, force_reload)
            except Exception as e:
                msg = """Error occurs when import component '{}': {}.\n
                Please make sure all requirements inside conda.yaml has been installed."""
                raise ImportException(message=msg.format(py_module, e)) from e

        objects_with_source_line_order = sorted(
            inspect.getmembers(py_module, inspect.isfunction), key=lambda x: inspect.getsourcelines(x[1])[1]
        )

        EXECUTOR_CLASS = cls._get_executor_class()
        for _, obj in objects_with_source_line_order:
            if cls._look_like_component(obj):
                component = EXECUTOR_CLASS(obj)
                component._check_py_module_valid(py_module)
                yield component

    @classmethod
    def _look_like_component(cls, f):
        """Return True if f looks like a component."""
        if not isinstance(f, types.FunctionType):
            return False
        if not hasattr(f, cls.INJECTED_FIELD):
            return False
        return True

    @classmethod
    def _get_executor_class(cls):
        try:
            from mldesigner._dependent_component_executor import DependentComponentExecutor

            return DependentComponentExecutor
        except ImportException:
            return ComponentExecutor

    @abstractmethod
    def _refresh_instance(self, func: types.FunctionType):
        """Refresh current instance with new function."""

    def _check_py_module_valid(self, py_module):
        """Check whether the entry py module is valid to make sure it could be run in AzureML."""

    def _update_func(self, func: types.FunctionType):
        # Set the injected field so the function could be used to initializing with `ComponentExecutor(func)`
        setattr(func, self.INJECTED_FIELD, self._raw_entity_args)

    def _reload_func(self):
        """Reload the function to make sure the latest code is used to generate yaml."""
        f = self._func
        module = importlib.import_module(f.__module__)
        # if f.__name__ == '__main__', reload will throw an exception
        if f.__module__ != "__main__":
            from mldesigner._utils import _force_reload_module

            _force_reload_module(module)
        func = getattr(module, f.__name__)
        self._func = func._func if _is_mldesigner_component(func) else func
        self._refresh_instance(self._func)

    def execute(self, args: dict = None):
        """Execute the component with arguments."""
        execute_logger.info("Provided args: '%s'", args)
        args = self._parse(args)
        execute_logger.info("Parsed args: '%s'", args)
        param_args, return_args = {}, {}
        # Split outputs specified by param and by return annotation
        for k, v in args.items():
            if k in self._return_mapping:
                return_args[k] = v
            else:
                param_args[k] = v

        # In case component function import other modules inside the function, need file directory in sys.path
        file_dir = str(Path(self._entry_file).parent)
        with inject_sys_path(file_dir):
            execute_logger.info("====================== User Logs ======================")
            res = self._func(**param_args)
            execute_logger.info("==================== User Logs End ====================")

            if return_args:
                self.finalize(res, return_args)

        if res is not None:
            # If user specified return annotation, self._execution_outputs['output'] is file path named xxx/output
            # otherwise, self._execution_outputs['output'] is the return value of the function
            if self.DEFAULT_OUTPUT_NAME not in self._execution_outputs:
                self._execution_outputs[self.DEFAULT_OUTPUT_NAME] = res

        return self._execution_outputs

    def finalize(self, run_result, return_args):
        """Write file for outputs specified by return annotation, write RH for control outputs."""
        # Convert run_result to mapping
        supported_result_types = (int, bool, float, str)
        if isinstance(run_result, supported_result_types):
            key = list(self._return_mapping.keys())[0]
            run_result_mapping = {key: run_result}
        else:
            raise UserErrorException(
                f"Unsupported return type {type(run_result)!r} of function "
                f"{self._func.__name__!r}, only primitive type {supported_result_types} is supported."
            )

        # Write outputs to file for outputs specified by return annotation
        execute_logger.info("Writing primitive outputs: '%s' to file", return_args)
        for key, path in return_args.items():
            if key not in run_result_mapping:
                raise UserErrorException(f"Output with name {key!r} not found in run result {run_result_mapping}.")
            path = Path(path)
            if path.exists() and path.is_dir():
                path = path / "output"  # refer to a file path if receive directory
            Path(path).write_text(str(run_result_mapping[key]))

        control_output_keys = [key for key, output in self._return_mapping.items() if output.is_control]
        if control_output_keys:
            # write control outputs into run properties with mlflow
            # TODO(1955852): handle control outputs for mldesigner execute
            control_output_content = json.dumps(
                {k: v for k, v in run_result_mapping.items() if k in control_output_keys}
            )
            self._write_control_outputs_to_run_history(control_output_content=control_output_content)

    def _parse(self, args):
        """Validate args and parse with arg_mapping"""
        if isinstance(self._execution_args, dict):
            args = self._execution_args if not isinstance(args, dict) else {**self._execution_args, **args}

        refined_args = {}
        # validate parameter name, replace '-' with '_' when parameters come from command line
        for k, v in args.items():
            if not isinstance(k, str):
                raise UserErrorException(f"Execution args name must be string type, got {type(k)!r} instead.")
            new_key = k.replace("-", "_")
            if not new_key.isidentifier():
                raise UserErrorException(f"Execution args name {k!r} is not a valid python identifier.")
            refined_args[new_key] = v

        return self._parse_with_mapping(refined_args, self._arg_mapping)

    @classmethod
    def _has_mldesigner_arg_mapping(cls, arg_mapping):
        for val in arg_mapping.values():
            if isinstance(val, (Input, Output)):
                return True
        return False

    def _parse_with_mapping(self, args, arg_mapping):
        """Use the parameters' info in arg_mapping to parse commandline params.

        :param args: A dict contains the actual param value for each parameter {'param-name': 'param-value'}
        :param arg_mapping: A dict contains the mapping from param key 'param_name' to _ComponentBaseParam
        :return: params: The parsed params used for calling the user function.

        Note: arg_mapping can be either azure.ai.ml.Input or mldesigner.Input, both will be handled here
        """
        # according to param definition, update actual arg or fill with default value
        self._refine_args_with_original_parameter_definition(args, arg_mapping)

        # If used with azure.ai.ml package,
        # all mldesigner Inputs/Outputs will be transformed to azure.ai.ml Inputs/Outputs
        # This flag helps to identify if arg_mapping is parsed with mldesigner io (standalone mode)
        has_mldesigner_io = self._has_mldesigner_arg_mapping(arg_mapping)
        # Convert the string values to real params of the function.
        params = {}
        for name, param in arg_mapping.items():
            type_name = type(param).__name__
            val = args.pop(param.name, None)
            # 1. If current param has no value
            if val is None:
                # Note: here param value only contains user input except default value on function
                if type_name == "Output" or not param.optional:
                    raise RequiredParamParsingError(name=param.name)
                # If the Input is optional and no value set from args, set it as None for function to execute
                if type_name == "Input" and param.optional is True:
                    params[name] = None
                continue

            # 2. If current param has value:
            #       If it is a parameter, we help the user to parse the parameter, if it is an input port,
            #       we use load to get the param value of the port, otherwise we just pass the raw value.
            param_value = val

            # 2a. For Input params, parse primitive params to proper type, for other type Input, keep it as string
            if type_name == "Input" and param._is_primitive_type:
                try:
                    # Two situations are handled differently: mldesigner.Input and azure.ai.ml.Input
                    param_value = (
                        IoConstants.PRIMITIVE_STR_2_TYPE[param.type](val)
                        if has_mldesigner_io
                        else param._parse_and_validate(val)
                    )
                except Exception:
                    raise UserErrorException(
                        f"Parameter transition for {param.name!r} failed: "
                        f"{val!r} can not be casted to type {param.type!r}"
                    )
            params[name] = param_value

            # 2b. For Output params, create dir for output path
            if type_name == "Output" and param.type == AssetTypes.URI_FOLDER and not Path(val).exists():
                Path(val).mkdir(parents=True, exist_ok=True)

        # used to notify user for additional args that are useless
        self._additional_args = args
        return params

    def _refine_args_with_original_parameter_definition(self, args, arg_mapping):
        """According to param definition, update actual arg or fill with default value.

        :param args: The actual args passed to execute component, need to be updated in this function.
        :type args: dict
        :param arg_mapping: Original parameters definition. Values are Input/Output objects.
        :type arg_mapping: dict

        Note: arg_mapping can be either azure.ai.ml.Input or mldesigner.Input, both will be handled here
        """

        self._execution_outputs = {}
        for _, param in arg_mapping.items():
            type_name = type(param).__name__
            # work 1: Update args inputs with default value like "max_epocs=10".
            # Currently we only consider parameter as an optional parameter when user explicitly specified optioanl=True
            # in parameter's annotation like this: "max_epocs(type="integer", optional=True, default=10)". But we still
            # have to handle case like "max_epocs=10"
            if (
                # When used with main package, EnumInput needs to be handled
                type_name in ("Input", "EnumInput")
                and param.name not in args
                and param._is_primitive_type is True
                and param.default is not None
            ):
                args[param.name] = param.default

            # work 2: Update args outputs to ComponentName_timestamp/output_name
            # if output is not specified, mldesigner will generate an output path automatically
            if type_name == "Output":
                if param.name not in args:
                    # if output path not specified, set as parameter name
                    args[param.name] = param.name
                self._execution_outputs[param.name] = str(Path(args[param.name]).resolve().absolute())

    @classmethod
    def _get_output_annotations(cls, func, mapping: dict):
        """Analyze the annotation of the function to get the parameter mapping dict and the output port list.
        :param func:
        :return: (param_mapping, output_list)
            param_mapping: The mapping from function param names to input ports/component parameters;
            output_list: The output port list analyzed from return annotations.
        """
        # Outputs defined by return annotation will be added into mapping
        return_mapping = cls._get_outputs_from_return_annotation(func)

        for key, definition in return_mapping.items():
            if key in mapping:
                raise UserErrorException(
                    f"Duplicate output {key!r} found in both parameters "
                    f"and return annotations of function {func.__name__!r}."
                )
            mapping[key] = definition
        return return_mapping

    @classmethod
    def _get_outputs_from_return_annotation(cls, func):
        """Convert return annotation to Outputs.

        Supported type:
            1. dsl output type. func() -> Output(type='boolean', is_control=True) will be keep as they are.

        Note:
            - Single output will be named as 'output'.
        """

        return_annotation = inspect.signature(func).return_annotation
        exception_tail = f"in return annotation of function {func.__name__!r}"

        if return_annotation is inspect.Parameter.empty:
            return {}

        if isinstance(return_annotation, cls.SUPPORTED_RETURN_TYPES):
            if return_annotation.type not in list(SupportedParameterTypes):
                raise UserErrorException(
                    f"Unsupported output type {return_annotation.type!r} {exception_tail}, "
                    f"expected types: {cls.SUPPORTED_RETURN_TYPES})."
                    f'e.g. func()-> Output(type="boolean")'
                )
            return_annotation.name = cls.DEFAULT_OUTPUT_NAME
            return {cls.DEFAULT_OUTPUT_NAME: return_annotation}

        raise UserErrorException(
            f"Unsupported type {return_annotation!r} {exception_tail}, "
            f'expected are primitive type dsl.types objects. e.g. func() -> Output(type="boolean")'
        )

    @classmethod
    def _update_environment(cls, environment_dict: dict, return_annotation: dict):
        """Add mlflow dependency if control output exists. If failed to update, environment will be kept as it is."""
        if not isinstance(environment_dict, dict):
            return environment_dict

        def has_dependency(dependency: str, dependencies_list: list):
            for dep in dependencies_list:
                if dep.startswith(dependency):
                    return True
            return False

        # copy env dict to avoid modifying the original one
        environment_dict = copy.deepcopy(environment_dict)
        mlflow_dependency = ["mlflow", "azureml-mlflow"]
        has_control_output = bool(any([getattr(o, "is_control", False) for o in return_annotation.values()]))
        if not has_control_output:
            return environment_dict
        try:
            deps = environment_dict["conda_file"]["dependencies"]
            for dep in deps:
                if isinstance(dep, dict) and "pip" in dep:
                    for mlflow_dep in mlflow_dependency:
                        if not has_dependency(mlflow_dep, dep["pip"]):
                            dep["pip"].append(mlflow_dep)
        except (AttributeError, KeyError):
            pass
        return environment_dict

    @classmethod
    def _write_control_outputs_to_run_history(cls, control_output_content: str):
        """Write control output content to run history."""
        execute_logger.info("Writing control outputs: '%s' to run history", control_output_content)

        try:
            import mlflow
            from mlflow.tracking import MlflowClient
            from mlflow.utils.rest_utils import http_request

        except ImportError as e:
            raise ImportError("mlflow is required to write control outputs. Please install mlflow first.") from e

        # step1: get mlflow run
        with mlflow.start_run() as run:
            client = MlflowClient()

            # step2: get auth
            cred = client._tracking_client.store.get_host_creds()

            # step3: update host to run history
            cred.host = cred.host.replace(
                "api.azureml.ms",
                "experiments.azureml.net",
            ).replace("mlflow/v1.0", "history/v1.0")

            # step4: call run history
            http_request(
                host_creds=cred,
                endpoint="/experimentids/{}/runs/{}".format(run.info.experiment_id, run.info.run_id),
                method="PATCH",
                json={
                    "runId": run.info.run_id,
                    "properties": {cls.CONTROL_OUTPUTS_KEY: control_output_content},
                },
            )
            execute_logger.info("Finished writing control outputs: '%s'", control_output_content)


class ComponentExecutor(ExecutorBase):
    """An executor to analyze the entity args of a function and convert it to a runnable component in AzureML."""

    def __init__(self, func: types.FunctionType, entity_args=None, _entry_file=None):
        """Initialize a ComponentExecutor with a function to enable calling the function with command line args.

        :param func: A function wrapped by mldesigner.component.
        :type func: types.FunctionType
        """
        if isinstance(func, types.FunctionType):
            arg_mapping = self._standalone_analyze_annotations(func)
        else:
            arg_mapping = {}
        super().__init__(func=func, entity_args=entity_args, _entry_file=_entry_file, arg_mapping=arg_mapping)

    @classmethod
    def _standalone_analyze_annotations(cls, func):
        mapping = _standalone_get_param_with_standard_annotation(func)
        return mapping

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

        # Indicate the component is generated by mldesigner
        tags[ExecutorBase.CODE_GEN_BY_KEY] = ComponentSource.MLDESIGNER.lower()
        entity_args["tags"] = tags

        if "type" in entity_args and entity_args["type"] == "SweepComponent":
            return entity_args

        entity_args["environment"] = cls._update_environment(entity_args.get("environment", None), return_annotation)
        entity_args["distribution"] = entity_args.get("distribution", None)
        return entity_args

    @classmethod
    def _refine_environment(cls, environment, mldesigner_component_source_dir):
        return environment

    def _refresh_instance(self, func: types.FunctionType):
        self.__init__(self._func, entity_args=self._raw_entity_args, _entry_file=self._entry_file)
