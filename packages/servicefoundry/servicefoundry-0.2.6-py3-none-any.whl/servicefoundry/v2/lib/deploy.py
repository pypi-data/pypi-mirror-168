from typing import List, TypeVar

from pydantic import BaseModel

from servicefoundry.auto_gen import models as auto_gen_models
from servicefoundry.lib.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.lib.dao.workspace import get_workspace_by_fqn
from servicefoundry.logger import logger
from servicefoundry.v2.lib.models import BuildResponse, Deployment
from servicefoundry.v2.lib.source import local_source_to_remote_source

Component = TypeVar("Component", bound=BaseModel)


def _upload_component_source_if_local(
    component: Component, workspace_fqn: str
) -> Component:
    if (
        hasattr(component, "image")
        and isinstance(component.image, auto_gen_models.Build)
        and isinstance(component.image.build_source, auto_gen_models.LocalSource)
    ):
        new_component = component.copy(deep=True)

        logger.info("Uploading code for %s '%s'", component.type, component.name)

        new_component.image.build_source = local_source_to_remote_source(
            local_source=component.image.build_source,
            workspace_fqn=workspace_fqn,
            component_name=component.name,
        )

        logger.debug("Uploaded code for %s '%s'", component.type, component.name)
        return new_component
    return component


def _log_hosts_for_services(deployment: Deployment):
    base_domain_url = deployment.baseDomainURL
    workspace_name = deployment.workspace.get("name", "")
    components = deployment.manifest.get("components", [])

    if not base_domain_url:
        logger.debug("Cannot print service hosts as baseDomainURL is empty")
        return

    if not workspace_name:
        logger.debug("Cannot print service hosts as workspace is empty")
        return

    for component in components:
        component_name = component.get("name", "")
        component_type = component.get("type", "")

        if component_type != "service":
            continue

        if not component_name:
            logger.debug("Cannot print service host as component name is empty")
            continue

        url = f"https://{component_name}-{workspace_name}.{base_domain_url}"
        logger.info(
            "Service '%s' will be available at\n'%s'\nafter successful deployment",
            component_name,
            url,
        )


def _log_application_dashboard_url(deployment: Deployment):
    application_id = deployment.applicationId

    # TODO: is there any simpler way to get this? :cry
    client = ServiceFoundryServiceClient.get_client()
    base_url = client.session.profile.server_config.base_url

    url = f"{base_url}/applications/{application_id}?tab=deployments"

    logger.info("You can find the application on the dashboard:- '%s'", url)


def _tail_build_logs(build_responses: List[BuildResponse]):
    client = ServiceFoundryServiceClient.get_client()

    # TODO: Explore other options like,
    # https://rich.readthedocs.io/en/stable/live.html#live-display
    # How does docker/compose does multiple build logs?
    for build_response in build_responses:
        logger.info("Tailing build logs for '%s'", build_response.componentName)
        client.tail_build_logs(build_response=build_response, wait=True)


def deploy_application(
    application: auto_gen_models.Application,
    workspace_fqn: str,
    wait: bool = False,
) -> Deployment:
    logger.info("Deploying application '%s' to '%s'", application.name, workspace_fqn)

    # print(application.yaml())
    workspace_id = get_workspace_by_fqn(workspace_fqn).id
    updated_component_definitions = []

    for component in application.components:
        updated_component = _upload_component_source_if_local(
            component=component, workspace_fqn=workspace_fqn
        )
        updated_component_definitions.append(updated_component)

    new_application_definition = auto_gen_models.Application(
        name=application.name, components=updated_component_definitions
    )
    client = ServiceFoundryServiceClient.get_client()
    response = client.deploy_application(
        workspace_id=workspace_id, application=new_application_definition
    )
    logger.info(
        "Deployment started for application '%s'. Deployment FQN is '%s'",
        application.name,
        response.fqn,
    )
    # TODO: look at build and deploy status
    # If there was any error, put error messages accordingly
    if wait:
        _tail_build_logs(build_responses=response.builds)
    _log_hosts_for_services(deployment=response)
    _log_application_dashboard_url(deployment=response)
    return response


def deploy_component(
    component: Component, workspace_fqn: str, wait: bool = False
) -> Deployment:
    application = auto_gen_models.Application(
        name=component.name, components=[component]
    )
    return deploy_application(
        application=application,
        workspace_fqn=workspace_fqn,
        wait=wait,
    )
