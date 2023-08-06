from typing import Optional

from servicefoundry.cli.console import console
from servicefoundry.lib.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.lib.messages import PROMPT_USING_WORKSPACE_CONTEXT
from servicefoundry.lib.model.entity import NewDeployment
from servicefoundry.lib.util import resolve_workspace_or_error


def list_application(
    workspace_fqn: Optional[str] = None,
    client: Optional[ServiceFoundryServiceClient] = None,
):
    client = client or ServiceFoundryServiceClient.get_client()
    if not workspace_fqn:
        deployments = client.list_applications()
    else:
        workspace, _ = resolve_workspace_or_error(
            name_or_id=workspace_fqn,
            non_interactive=True,
            cluster_name_or_id=None,
            client=client,
        )
        console.print(PROMPT_USING_WORKSPACE_CONTEXT.format(workspace.name))
        deployments = client.list_applications(workspace.id)
    deployments = [NewDeployment.from_dict(d) for d in deployments]
    return deployments
