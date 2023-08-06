# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import List


def export(source: str, include_components: List[str] = None):  # pylint: disable=unused-argument
    """Export pipeline source to code.

    :param source: Pipeline job source, currently supported format is pipeline run URL
    :param include_components: Included components to download snapshot.
        Use * to export all components,
        Or list of components used in pipeline.
        If not specified, all components in pipeline will be exported without downloading snapshot.
    :return:
    """
