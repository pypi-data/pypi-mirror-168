import logging
import os
import sys
from pathlib import Path

from rowantree.common.sdk import demand_env_var


def get_log_params(to_file: bool = False) -> dict:
    params = {
        "level": logging.DEBUG,
        "format": "%(asctime)s - %(levelname)s - %(message)s",
        "datefmt": "%m/%d/%Y %I:%M:%S %p",
    }

    if to_file:
        params["filename"] = f"{demand_env_var(name='LOGS_DIR')}/{os.uname()[1]}.therowantree.content.service.log"
        params["filemode"] = "w"
    else:
        params["stream"] = sys.stdout

    return params


def setup_logging(to_file: bool = False) -> None:
    # Setup logging
    if to_file:
        Path(demand_env_var(name="LOGS_DIR")).mkdir(parents=True, exist_ok=True)

    params = get_log_params(to_file=to_file)
    logging.basicConfig(**params)
