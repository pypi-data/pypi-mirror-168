# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import List

from azure.ai.ml import MLClient
from azure.ai.ml.entities._builders import Command, Pipeline
from mldesigner._exceptions import UserErrorException
from mldesigner._export._parse_url import _parse_designer_url
from mldesigner._utils import get_credential_auth


def _export(source: str, include_components: List[str] = None):  # pylint: disable=unused-argument
    """Export pipeline source to code.

    :param source: Pipeline job source, currently supported format is pipeline run URL
    :param include_components: Included components to download snapshot.
        Use * to export all components,
        Or list of components used in pipeline.
        If not specified, all components in pipeline will be exported without downloading snapshot.
    :return:
    """
    # get subscription_id, resource_group, workspace_name, run_id from url
    (
        subscription_id,
        resource_group,
        workspace_name,
        draft_id,
        run_id,
        endpoint_id,
        published_pipeline_id,
        graph_id,  # pylint: disable=unused-variable
    ) = _parse_designer_url(source)

    # validate: raise error when the job type is not pipeline job
    if draft_id:
        raise UserErrorException("Invalid url. Export pipeline draft is not supported.")
    if endpoint_id:
        raise UserErrorException("Invalid url. Export pipeline endpoint is not supported.")
    if published_pipeline_id:
        raise UserErrorException("Invalid url. Export published pipeline is not supported.")

    credential = get_credential_auth()

    # get pipeline entity
    client = MLClient(
        credential=credential,
        resource_group_name=resource_group,
        subscription_id=subscription_id,
        workspace_name=workspace_name,
    )
    job_entity = client.jobs.get(run_id)

    # validate: raise error when the pipeline job contain subgraph
    if len(job_entity.jobs) == 0:
        raise UserErrorException("Failed to fetch pipeline nodes")
    for node in job_entity.jobs.values():  # pylint: disable=no-member
        # check whether this component has subgraph
        # pylint: disable=unidiomatic-typecheck
        if type(node) == Command:
            # generate a new yml to write down the component (further work)
            pass
            # generate
        if type(node) == Pipeline:
            # TODO: generate code for pipeline with subgraphs
            raise UserErrorException("Generating code for pipeline with subgraphs is not supported currently")
