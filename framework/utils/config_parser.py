from typing import Optional


def get_config_value(config: dict, key: str, required: bool = False, default: Optional[str] = None) -> Optional[str]:
    """
    Returns a config value by key. Raises an error if the key is required but missing or empty.

    :param config: Configuration dictionary.
    :param key: Key to look up.
    :param required: If True, raises an error when the key is missing or empty.
    :param default: Value to return if the key is optional and missing.
    :return: The config value or default.
    :raises ValueError: If a required key is missing or empty.
    """
    value = config.get(key, default)

    if required and not value:
        raise ValueError(f"Missing required config key: '{key}'")

    return value
