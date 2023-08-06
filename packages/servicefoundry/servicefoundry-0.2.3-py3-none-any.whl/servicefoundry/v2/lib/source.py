import os
import tempfile
from typing import Optional

from servicefoundry.auto_gen import models
from servicefoundry.lib.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.logger import logger
from servicefoundry.utils.file_utils import make_tarfile
from servicefoundry.v2.lib.patched_models import RemoteSource


def _get_ignorefile_path(source_dir: str) -> Optional[str]:
    ignore_file_path = os.path.join(source_dir, ".sfyignore")
    if os.path.exists(ignore_file_path):
        logger.info(".sfyignore file found!")
        return ignore_file_path

    logger.info(
        ".sfyignore not file found! We recommend you to create .sfyignore file and add file patterns to ignore"
    )
    return None


def local_source_to_remote_source(
    local_source: models.LocalSource,
    workspace_fqn: str,
    component_name: str,
) -> RemoteSource:
    with tempfile.TemporaryDirectory() as local_dir:
        package_local_path = os.path.join(local_dir, "build.tar.gz")
        source_dir = os.path.abspath(local_source.project_root_path)

        if not os.path.exists(source_dir):
            raise ValueError(
                f"project root path {source_dir!r} of component {component_name!r} does not exist"
            )

        logger.info("Uploading contents of %r", source_dir)

        ignorefile_path = _get_ignorefile_path(source_dir)

        make_tarfile(
            output_filename=package_local_path,
            source_dir=local_source.project_root_path,
            additional_directories=[],
            ignorefile_path=ignorefile_path,
        )
        client = ServiceFoundryServiceClient.get_client()
        presigned_url = client.upload_code_package(
            workspace_fqn=workspace_fqn,
            component_name=component_name,
            package_local_path=package_local_path,
        )
        return RemoteSource(remote_uri=presigned_url.presigned_url)
