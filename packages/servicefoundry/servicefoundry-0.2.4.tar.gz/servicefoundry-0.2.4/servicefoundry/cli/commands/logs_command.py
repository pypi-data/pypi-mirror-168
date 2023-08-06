import logging

import rich_click as click

from servicefoundry.cli.const import COMMAND_CLS
from servicefoundry.cli.util import handle_exception_wrapper
from servicefoundry.io.rich_output_callback import RichOutputCallBack
from servicefoundry.lib.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.lib.logs_utils import get_timestamp_from_timestamp_or_duration

logger = logging.getLogger(__name__)


@click.command(name="logs", cls=COMMAND_CLS)
@click.option(
    "--deployment-fqn", type=click.STRING, help="deployment fqn", required=True
)
@click.option(
    "--since",
    type=click.STRING,
    help="Show logs since timestamp (e.g.2013-01-02T13:23:37Z) or relative (e.g. 42m for 42 minutes)",
    default="2h",
)
@click.option(
    "--until",
    type=click.STRING,
    help="Show logs until timestamp (e.g.2013-01-02T13:23:37Z) or relative (e.g. 42m for 42 minutes)",
    default=None,
)
@click.option(
    "-n", "--tail", type=click.INT, help="Number of logs to tail", default=None
)
@click.option("-f", "--follow", help="Follow log output", is_flag=True, default=False)
@handle_exception_wrapper
def logs_command(deployment_fqn, since, until, tail, follow):
    """
    Get log tails for deployment fqn
    """
    start_ts = None
    end_ts = None
    if since:
        start_ts = get_timestamp_from_timestamp_or_duration(since)
    if until:
        end_ts = get_timestamp_from_timestamp_or_duration(until)

    output_hook = RichOutputCallBack()
    tfs_client = ServiceFoundryServiceClient.get_client()

    if until or not follow:
        tfs_client.fetch_deployment_logs(
            deployment_fqn=deployment_fqn,
            start_ts=start_ts,
            end_ts=end_ts,
            limit=tail,
            callback=output_hook,
        )
    else:
        tfs_client.tail_logs_for_deployment(
            deployment_fqn=deployment_fqn,
            start_ts=start_ts,
            limit=tail,
            callback=output_hook,
            wait=True,
        )


def get_logs_command():
    return logs_command
