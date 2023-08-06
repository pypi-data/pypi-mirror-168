from typing import Any, Callable, List, Optional, Tuple

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


def write_to_allen_config(
    key: str, value: Any, config_path: Optional[str] = ALLEN_CONFIG_PATH
) -> None:
    if not config_path or not os.path.isfile(config_path):
        raise NPTKError("Couldn't find config: %s" % config_path)

    with open(config_path) as f:
        config = json.load(f)

    config[key] = value

    with open(config_path, "w") as f:
        json.dump(config, f, indent=4, sort_keys=True)


def with_allen_config_fallback(
    values: List[Tuple[str, str]] = []
) -> Callable[..., Any]:
    """Use allen config if certain variables don't exist, best way to remove a logical statement from
    most of the code.

    Notes:
        Only overrides kwargs.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            for (name, config_name) in values:
                if kwargs.get(name) is None:
                    kwargs[name] = allen_config_auto_discovery(config_name)

            return func(*args, **kwargs)

        return wrapped

    return decorator
