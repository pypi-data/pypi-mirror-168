from typing import Any

import json
import os

from .exceptions import NPTKError

ALLEN_CONFIG_PATH = (
    "//allen/programs/braintv/workgroups/nc-ophys/1022/allen_auto_config.json"
)


def allen_config_auto_discovery(key: str, config_path: str = ALLEN_CONFIG_PATH) -> Any:
    """For ease of development at the institute, gets config values
    from a static path on the /allen network drive.

    Args:
        key: name of the config value to grab
        config_path: config filepath

    Returns:
        config value for key

    Raises:
        NPTKError: Config at `config_path` couldn't be found or the requested `key` doesn't exist.
    """
    if not os.path.isfile(config_path):
        raise NPTKError("Couldn't find config: %s" % config_path)

    with open(config_path) as f:
        config = json.load(f)

    try:
        return config[key]
    except KeyError:
        raise NPTKError("%s not found in allen config" % key)
