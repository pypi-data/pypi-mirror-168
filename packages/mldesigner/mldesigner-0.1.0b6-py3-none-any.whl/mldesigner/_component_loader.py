# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

# pylint: disable=unused-argument


def _overwrite_component_load_options(name, component):
    """If config file "components.yaml" exist in current folder, overwrite component load options with the config."""
    # TODO(1831493): support component loader
    return component
