import logging
import logging.config
import pathlib
import sys
from datetime import datetime
from typing import Dict, Any, Optional

import yaml

DEFAULT_CONFIG_FILE = pathlib.Path(__file__).parent / 'log_config.yaml'

LOGS_DIRECTORY = pathlib.Path('logs')
LOGS_DIRECTORY.mkdir(exist_ok=True)

DATETIME_FORMAT = "%Y-%m-%d %H-%M-%S"


def generate_log_filename(file_name: str = "test.log") -> str:
    """
    Generate a log filename with a timestamp prefix.

    :param file_name: Base log file name, including extension (e.g., 'test.log').
    :return: Timestamped log file name (e.g., '2025-05-04_15-45-30_test.log').
    """

    timestamp = datetime.now().strftime(DATETIME_FORMAT)
    return f"{timestamp}_{file_name}"


def load_config(config_path: pathlib.Path) -> Dict[str, Any]:
    """
    Load and parse the YAML logging configuration file.

    :param config_path: Path to the YAML logging config file.
    :return: Parsed configuration as a dictionary.
    """
    if not config_path.exists():
        raise FileNotFoundError(f"Logger config file '{config_path}' not found")

    with config_path.open('rt') as f:
        return yaml.safe_load(f)


def update_log_filenames(config: Dict[str, Any]) -> None:
    """
    Update the log filenames in the configuration, generating dynamic names based on the timestamp.

    :param config: Updated logging configuration.
    """
    log_handlers = config.get("handlers")
    if log_handlers:
        for handler in log_handlers.values():
            output_file = handler.get("filename")
            if output_file:
                # Dynamically generate log file names
                handler["filename"] = LOGS_DIRECTORY.joinpath(generate_log_filename(output_file))


def setup_logger(config_path: pathlib.Path = DEFAULT_CONFIG_FILE) -> None:
    """
    Configure logging using a YAML configuration file.

    :param config_path: Path to the YAML logging config file.
    """
    try:
        config = load_config(config_path)
        update_log_filenames(config)
        logging.config.dictConfig(config)

        sys.excepthook = unhandled_exception_handler

    except FileNotFoundError as e:
        logging.error(f"Logger config file was not found: {e}")
        raise

    except yaml.YAMLError as e:
        logging.error(f"Error parsing YAML config file: {e}")
        raise


def unhandled_exception_handler(exc_type: type, exc_value: Exception, exc_traceback: Optional[Any]) -> None:
    """Global unhandled exception handler."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger = logging.getLogger(__name__)
    logger.critical("Unhandled exception occurred", exc_info=(exc_type, exc_value, exc_traceback))
