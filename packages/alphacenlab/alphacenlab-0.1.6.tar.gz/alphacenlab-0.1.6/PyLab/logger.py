import logging
import logging.config


def initialize_logger(logging_config_file: str = "./logging.ini", log_level: str = "INFO") -> logging.RootLogger:
    """
    initialize the logger with the logging config file and set the logger level

    Args:
        logging_config_file: logging config file location
        log_level: Log level by logging, see https://docs.python.org/3/library/logging.html#levels

    Returns:
        root logger

    Raises:
        KeyError: Cannot find keys in logging_config_file
        AssertionError: log_level not supported 
    """
    assert log_level in ["CRITICAL", "ERROR",
                         "WARNING",  "INFO", "DEBUG",  "NOTSET"]

    logging.config.fileConfig(logging_config_file)
    new_logger = logging.getLogger()
    new_logger.setLevel(log_level)
    return new_logger
