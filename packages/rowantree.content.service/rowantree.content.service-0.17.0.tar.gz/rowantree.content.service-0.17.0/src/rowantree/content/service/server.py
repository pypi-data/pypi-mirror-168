""" Content Service Entry Point """

import logging
import sys

from rowantree.common.sdk import demand_env_var, demand_env_var_as_bool, demand_env_var_as_float, demand_env_var_as_int
from rowantree.game.service.sdk import RowanTreeService
from rowantree.game.service.sdk.contracts.dto.command_options import CommandOptions
from src.rowantree.content.service.utils.log import setup_logging

from .common.world.personality import WorldPersonality
from .common.world.storyteller import WorldStoryTeller


def handler():
    setup_logging(to_file=demand_env_var_as_bool("LOG_TO_FILE"))

    logging.debug("Starting service")

    options: CommandOptions = CommandOptions.parse_obj(
        {
            "sleep_time": demand_env_var_as_float("ROWANTREE_SERVICE_SLEEP_TIME"),
            "retry_count": demand_env_var_as_int("ROWANTREE_SERVICE_RETRY_COUNT"),
            "tld": demand_env_var("ROWANTREE_TLD"),
            "timeout": demand_env_var_as_float("ROWANTREE_SERVICE_TIMEOUT"),
        }
    )

    rowantree_service: RowanTreeService = RowanTreeService(options=options)
    loremaster_service: WorldStoryTeller = WorldStoryTeller()
    personality: WorldPersonality = WorldPersonality(
        rowantree_service=rowantree_service, loremaster_service=loremaster_service
    )

    logging.debug("Starting contemplation loop")
    while True:
        personality.contemplate()


if __name__ == "__main__":
    handler()
