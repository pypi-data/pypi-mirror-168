# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

# pylint: disable=redefined-builtin, unused-argument

from functools import wraps
from os import PathLike
from typing import Any, Callable, TypeVar, Union, get_type_hints

from mldesigner._component_loader import _overwrite_component_load_options

_TFunc = TypeVar("_TFunc", bound=Callable[..., Any])


def reference_component(path: Union[PathLike, str] = None, name=None, version=None, **kwargs) -> _TFunc:
    """Reference an existing component with a function and return a component node built with given params.
    The referenced component can be defined with local yaml file or in remote with name and version.
    The returned component node type are hint with function return annotation and default to Command.
    Eg: Both
    .. code-block:: python

        @reference_component()
        def my_func():
            ...
    and
    .. code-block:: python

        @reference_component()
        def my_func() -> Command:
            ...
    with return a Command node.
    .. code-block:: python

        @reference_component()
        def my_func() -> Parallel:
            ...
    will return a Parallel node.

    :param path: Path to local component file.
    :type path: str
    :param name: Name of component to load.
    :type name: str
    :param version: Version of component to load.
    :type version: str

    :return: Component node.
    :rtype: Union[Command, Parallel]
    """

    def component_decorator(func: _TFunc) -> _TFunc:
        @wraps(func)
        def wrapper(*args, **inner_kwargs):
            from azure.ai.ml import load_component
            from azure.ai.ml.dsl._dynamic import _assert_arg_valid
            from azure.ai.ml.entities._builders import Command
            from azure.ai.ml.entities._job.pipeline._exceptions import UserErrorException
            from mldesigner._generate._generators._constants import COMPONENT_TO_NODE

            if args:
                raise UserErrorException(
                    message="`reference_component` wrapped function only accept keyword parameters."
                )
            # handle params case insensitively, raise error when unknown kwargs are passed
            _assert_arg_valid(inner_kwargs, func.__code__.co_varnames, func_name=func.__name__)

            if path:
                # load from local
                component = load_component(source=path)
            else:
                # load from remote
                # use function name as component name if not specified
                component_name = name or func.__name__

                component = component_name if version is None else f"{component_name}:{version}"

            component = _overwrite_component_load_options(func.__name__, component)

            result_cls = get_type_hints(func).get("return", Command)

            # supported return annotations, traverse in order
            # Note: make sure no base node in supported_cls
            supported_cls = COMPONENT_TO_NODE.values()
            for cls in supported_cls:
                if issubclass(result_cls, cls):
                    result_cls = cls
            if result_cls not in supported_cls:
                msg = (
                    f"Return annotation of `reference_component` wrapped function can only be {supported_cls} "
                    f"or its subclass, got {result_cls} instead."
                )
                raise UserErrorException(message=msg)
            result = result_cls(component=component, inputs=inner_kwargs, _from_component_func=True)

            return result

        return wrapper

    return component_decorator
