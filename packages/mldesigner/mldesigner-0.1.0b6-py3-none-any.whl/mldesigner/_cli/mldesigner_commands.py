# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

# pylint: disable=line-too-long

import argparse
import sys

from mldesigner import generate
from mldesigner._execute._execute import _execute
from mldesigner._export._export import export
from mldesigner._utils import list_2_dict


def _entry(argv):
    """
    CLI tools for mldesigner.
    """
    parser = argparse.ArgumentParser(
        prog="mldesigner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="A CLI tool for mldesigner. [Preview]",
    )

    subparsers = parser.add_subparsers()

    add_parser_generate(subparsers)
    add_parser_execute(subparsers)
    add_export_sub_parser(subparsers)

    args = parser.parse_args(argv)

    if args.action == "generate":
        generate(source=args.source, package_name=args.package_name, force_regenerate=args.force)

    elif args.action == "execute":
        processed_inputs = list_2_dict(args.inputs)
        processed_outputs = list_2_dict(args.outputs)
        _execute(args.source, args.name, processed_inputs, processed_outputs)

    elif args.action == "export":
        export(source=args.source, include_components=args.include_components)


def add_parser_generate(subparsers):
    """The parser definition of mldesigner generate"""

    epilog_generate = """
    Examples:

    # generate component functions for existing package
    mldesigner generate --source components/**/*.yaml

    # generate component functions from workspace
    mldesigner generate --source azureml://subscriptions/xxx/resourcegroups/xxx/workspaces/xxx

    # generate component functions from dynamic source
    mldesigner generate --source azureml://subscriptions/xxx/resourcegroups/xxx/workspaces/xxx components/**/*.yml

    # generate component functions from dynamic source, source configured in mldesigner.yml
    mldesigner generate --source mldesigner.yml

    # generate package from workspace
    mldesigner generate --source azureml://subscriptions/xxx/resourcegroups/xxx/workspaces/xxx --package-name my-cool-package
    """
    generate_parser = subparsers.add_parser(
        "generate",
        description="A CLI tool to generate component package.",
        help="For a set of source, generate a python module which contains component consumption functions and import it for use.",
        epilog=epilog_generate,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    generate_parser.add_argument(
        "--source",
        nargs="+",
        type=str,
        help="List of source need to be generated or path of source config yaml.",
    )
    generate_parser.add_argument("--package-name", type=str, help="Name of the generated python package.")
    generate_parser.add_argument(
        "--force", action="store_true", help="If specified, will always regenerate package from given source."
    )
    generate_parser.set_defaults(action="generate")


def add_parser_execute(subparsers):
    """The parser definition of mldesigner execute"""

    epilog_execute = """
    Examples:

    # Basic execute command with source file specified:
    mldesigner execute --source ./components.py

    # Execute with specified component name and inputs:
    mldesigner execute --source ./components.py --name sum_component --inputs a=1 b=2"""

    execute_parser = subparsers.add_parser(
        "execute",
        description="A CLI tool to execute component.",
        help="Execute a component in local host environment, execute source is a mldesigner component file path.",
        epilog=epilog_execute,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    execute_parser.add_argument(
        "--source", required=True, help="The file path that contains target mldesigner component to be executed."
    )
    execute_parser.add_argument(
        "--name",
        required=False,
        help=(
            "The component name of the target to be executed. Note it's not the function name but the component name. "
            "If not specified, will execute the first component inside the source file."
        ),
    )
    execute_parser.add_argument(
        "--inputs",
        nargs="*",
        required=False,
        help=("The input parameters for component to execute. (e.g.) '--inputs a=1 b=2'"),
    )
    execute_parser.add_argument(
        "--outputs",
        nargs="*",
        required=False,
        help=(
            "The customizable output path for component execution results. This is only meaningful when the component "
            "has 'uri_folder' or 'uri_file' output parameters. If not specified, output path will be the parameter name. "
            "(e.g.) '--outputs a=path0 b=path1'"
        ),
    )
    execute_parser.set_defaults(action="execute")


def add_export_sub_parser(subparsers):
    # mldesigner export

    example_text = """
    Examples:

    # export pipeline run to code without component snapshot by URL
    mldesigner export --source pipeline_run_url

    # export full snapshot of a pipeline run by URL
    mldesigner export --source pipeline_run_url --include-components "*"

    # export pipeline with selected component snapshot by URL
    mldesigner export --source pipeline_run_url --include-components train:0.0.1 anonymous_component:guid_version
    """
    generate_parser = subparsers.add_parser(
        "export",
        description="A CLI tool to export UI graph to azure-ai-ml code.",
        help="mldesigner export",
        epilog=example_text,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    generate_parser.add_argument(
        "--source",
        type=str,
        help="""Pipeline job source, currently supported format is pipeline run URL""",
    )
    generate_parser.add_argument(
        "--include-components",
        nargs="+",
        type=str,
        help="""Included components to download snapshot. Use * to export all components;
        Or separated string which contains a subset of components used in pipeline.
        Provided components can be name:version to download specific version of component
        or just name to download all versions of that component.""",
    )
    generate_parser.set_defaults(action="export")


def main():
    """Entrance of mldesigner CLI."""
    command_args = sys.argv[1:]
    if len(command_args) == 0:
        command_args.append("-h")
    _entry(command_args)
