from logging.config import dictConfig

from src.settings import config


def setup_logging():
    formatters = {
        "console": {
            "class": "logging.Formatter",
            "datefmt": "%Y-%m-%dT%H:%M:%S",
            "format": "%(name)s:%(lineno)d - %(message)s",
        }
    }

    handlers = {
        "default": {
            "class": "rich.logging.RichHandler",
            "level": config.LOG_LEVEL,
            "formatter": "console",
            "show_path": False,
        }
    }

    # Declare src logger as the root logger
    # Any other loggers will be children of src and inherit the settings
    loggers = {
        "src": {"level": config.LOG_LEVEL, "handlers": ["default"], "propagate": False}
    }

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": formatters,
            "handlers": handlers,
            "loggers": loggers,
        }
    )
