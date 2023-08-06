# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import contextlib
import importlib
import inspect
import logging
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import pkg_resources

from mldesigner._constants import MLDESIGNER_COMPONENT_EXECUTION, VALID_NAME_CHARS
from mldesigner._exceptions import ComponentException, UserErrorException
from mldesigner._logger_factory import _LoggerFactory


def is_valid_name(name: str):
    """Indicate whether the name is a valid component name."""
    return all(c in VALID_NAME_CHARS for c in name)


def _resolve_source_directory():
    """Resolve source directory as last customer frame's module file dir position."""
    source_file = _resolve_source_file()
    # Fall back to current working directory if not found
    return Path(os.getcwd()) if not source_file else Path(os.path.dirname(source_file)).absolute()


def _resolve_source_file():
    """Resolve source file as last customer frame's module file position."""
    try:
        frame_list = inspect.stack()
        # We find the last frame which is in SDK code instead of customer code or dependencies code
        # by checking whether the package name of the frame belongs to azure.ai.ml.component.
        pattern = r"(^mldesigner(?=\..*|$).*)"
        for frame, last_frame in zip(frame_list, frame_list[1:]):
            if _assert_frame_package_name(pattern, frame.frame) and not _assert_frame_package_name(
                pattern, last_frame.frame
            ):
                module = inspect.getmodule(last_frame.frame)
                return Path(module.__file__).absolute() if module else None
    # pylint: disable=broad-except
    except Exception:
        return None


def _assert_frame_package_name(pattern, frame):
    """Check the package name of frame is match pattern."""
    # f_globals records the function's module globals of the frame. And __package__ of module must be set.
    # https://docs.python.org/3/reference/import.html#__package__
    # Although __package__ is set when importing, it may happen __package__ does not exist in globals
    # when using exec to execute.
    package_name = frame.f_globals.get("__package__", "")
    return bool(package_name and re.match(pattern, package_name))


def _mldesigner_component_execution() -> bool:
    """Return True if mldesigner component is executing."""
    if os.getenv(MLDESIGNER_COMPONENT_EXECUTION, "false").lower() == "true":
        return True
    return False


def _relative_to(path, basedir, raises_if_impossible=False):
    """Compute the relative path under basedir.

    This is a wrapper function of Path.relative_to, by default Path.relative_to raises if path is not under basedir,
    In this function, it returns None if raises_if_impossible=False, otherwise raises.

    """
    # The second resolve is to resolve possible win short path.
    path = Path(path).resolve().absolute().resolve()
    basedir = Path(basedir).resolve().absolute().resolve()
    try:
        return path.relative_to(basedir)
    except ValueError:
        if raises_if_impossible:
            raise
        return None


def _is_mldesigner_component(function):
    return hasattr(function, "_is_mldesigner_component")


@contextlib.contextmanager
def _change_working_dir(path, mkdir=True):
    """Context manager for changing the current working directory"""

    saved_path = os.getcwd()
    if mkdir:
        os.makedirs(path, exist_ok=True)
    os.chdir(str(path))
    try:
        yield
    finally:
        os.chdir(saved_path)


def _import_component_with_working_dir(module_name, working_dir=None, force_reload=False):
    if working_dir is None:
        working_dir = os.getcwd()
    working_dir = str(Path(working_dir).resolve().absolute())

    with _change_working_dir(working_dir, mkdir=False), inject_sys_path(working_dir):
        try:
            py_module = importlib.import_module(module_name)
        except Exception as e:
            raise e
        except BaseException as e:
            # raise base exception like system.exit as normal exception
            raise ComponentException(message=str(e)) from e
        loaded_module_file = Path(py_module.__file__).resolve().absolute().as_posix()
        posix_working_dir = Path(working_dir).absolute().as_posix()
        if _relative_to(loaded_module_file, posix_working_dir) is None:
            if force_reload:
                # If force_reload is True, reload the module instead of raising exception.
                # This is used when we don't care the original module with the same name.
                return importlib.reload(py_module)
            raise RuntimeError(
                "Could not import module: '{}' because module with the same name has been loaded.\n"
                "Path of the module: {}\n"
                "Working dir: {}".format(module_name, loaded_module_file, posix_working_dir)
            )
        return py_module


@contextlib.contextmanager
def inject_sys_path(path):
    path_str = str(path)
    sys.path.insert(0, path_str)
    try:
        yield
    finally:
        if path_str in sys.path:
            sys.path.remove(path_str)


def _force_reload_module(module):
    # Reload the module except the case that module.__spec__ is None.
    # In the case module.__spec__ is None (E.g. module is __main__), reload will raise exception.
    if module.__spec__ is None:
        return module
    path = Path(module.__spec__.loader.path).parent
    with inject_sys_path(path):
        return importlib.reload(module)


@contextlib.contextmanager
def environment_variable_overwrite(key, val):
    if key in os.environ.keys():
        backup_value = os.environ[key]
    else:
        backup_value = None
    os.environ[key] = val

    try:
        yield
    finally:
        if backup_value:
            os.environ[key] = backup_value
        else:
            os.environ.pop(key)


def _is_primitive_type(val):
    return val in (int, float, bool, str)


def _sanitize_python_class_name(snake_name: str):
    """Change variable name from snake to camel case."""
    components = snake_name.split("_")
    return "".join(component.title() for component in components)


class TimerContext(object):
    """A context manager calculates duration when executing inner block."""

    def __init__(self):
        self.start_time = None

    def get_duration_seconds(self):
        """Get the duration from context manger start to this function call.
        Result will be format to two decimal places.

        """
        duration = datetime.utcnow() - self.start_time
        return round(duration.total_seconds(), 2)

    def __enter__(self):
        self.start_time = datetime.utcnow()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


@contextlib.contextmanager
def update_logger_level(level):
    logger = logging.getLogger()
    backup_level = logger.level

    logger.setLevel(level)

    try:
        yield
    finally:
        logger.setLevel(backup_level)


def list_2_dict(input_list):
    """Transform a list ['a=1', 'b=2'] to dict {'a'='1', 'b'='2'}."""
    if input_list is None:
        return None
    res = {}
    try:
        for item in input_list:
            key, value = item.split("=")
            res[key] = value
    except Exception as e:
        raise UserErrorException(
            "Incorrect parameter format. Please make sure command arguments are like '--inputs a=1 b=2' "
            "or '--outputs a=path0 b=path1'"
        ) from e
    return res


def get_package_version(package_name):
    """Get the version of the package."""
    try:
        return pkg_resources.get_distribution(package_name).version
    except pkg_resources.DistributionNotFound:
        return None


def check_main_package(logger=None):
    if logger is None:
        logger = _LoggerFactory.get_logger("mldesigner")
    version = get_package_version("azure-ai-ml")
    target_version = "0.1.0b7"
    version_to_check = pkg_resources.parse_version(target_version)
    msg = (
        f"Mldesigner requires azure-ai-ml >= {target_version} package to be fully functional."
        f"It's highly recommended to install the latest azure-ai-ml package."
    )
    if version:
        if not version.startswith("0.0."):
            # public version
            if pkg_resources.parse_version(version) <= version_to_check:
                logger.warning(msg)
    else:
        logger.warning(msg)


def get_credential_auth():
    """Get the available credential."""
    from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential

    try:
        credential = DefaultAzureCredential()
        # Check if given credential can get token successfully.
        credential.get_token("https://management.azure.com/.default")
    except Exception:  # pylint: disable=broad-except
        # Fall back to InteractiveBrowserCredential in case DefaultAzureCredential not work
        credential = InteractiveBrowserCredential()
    return credential
