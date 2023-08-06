""" Content Service Entry Point """

import logging
import os
from pathlib import Path

from rowantree.common.sdk import demand_env_var, demand_env_var_as_float, demand_env_var_as_int
from rowantree.game.service.sdk import RowanTreeService
from rowantree.game.service.sdk.contracts.dto.command_options import CommandOptions

from .common.world.personality import WorldPersonality
from .common.world.storyteller import WorldStoryTeller

if __name__ == "__main__":
    # Setup logging
    Path(demand_env_var(name="LOGS_DIR")).mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        level=logging.DEBUG,
        filemode="w",
        filename=f"{demand_env_var(name='LOGS_DIR')}/{os.uname()[1]}.therowantree.content.service.log",
    )

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
