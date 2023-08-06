import os
import tempfile
from typing import Callable, Optional

import gitignorefile

from servicefoundry.auto_gen import models
from servicefoundry.lib.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.logger import logger
from servicefoundry.utils.file_utils import make_tarfile
from servicefoundry.v2.lib.patched_models import RemoteSource


def _get_callback_handler_to_ignore_file_path(
    source_dir: str,
) -> Optional[Callable[[str], bool]]:
    ignorefile_path = os.path.join(source_dir, ".sfyignore")
    if os.path.exists(ignorefile_path):
        logger.info(".sfyignore file found in %s", source_dir)
        return gitignorefile.parse(path=ignorefile_path, base_path=source_dir)

    # check for valid git repo
    try:
        import git

        repo = git.Repo(source_dir, search_parent_directories=True)
        return lambda file_path: repo.ignored([file_path])
    except Exception as ex:
        logger.debug(
            "Could not treat source %r as a git repository due to %r", source_dir, ex
        )

    logger.info(
        "Neither `.sfyignore` file found in %s nor a valid git repository found. We recommend you to create .sfyignore file and add file patterns to ignore",
        source_dir,
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

        is_path_ignored = _get_callback_handler_to_ignore_file_path(source_dir)

        make_tarfile(
            output_filename=package_local_path,
            source_dir=source_dir,
            additional_directories=[],
            is_path_ignored=is_path_ignored,
        )
        client = ServiceFoundryServiceClient.get_client()
        presigned_url = client.upload_code_package(
            workspace_fqn=workspace_fqn,
            component_name=component_name,
            package_local_path=package_local_path,
        )
        return RemoteSource(remote_uri=presigned_url.presigned_url)
