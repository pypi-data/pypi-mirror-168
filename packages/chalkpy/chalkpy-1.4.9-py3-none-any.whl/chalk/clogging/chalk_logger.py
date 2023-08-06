import logging.config

from log_with_context import Logger

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {"()": "json_log_formatter.JSONFormatter"},
        },
        "handlers": {
            "console": {
                "formatter": "json",
                "class": "logging.StreamHandler",
            }
        },
        "loggers": {
            "": {"handlers": ["console"], "level": "DEBUG"},
        },
    }
)

chalk_logger = Logger(__name__)
