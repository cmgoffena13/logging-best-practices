from logging.config import dictConfig

from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

from src.settings import ProdConfig, config


def setup_logging():
    logger_provider = LoggerProvider()
    set_logger_provider(logger_provider)

    if isinstance(config, ProdConfig):
        # Setup OpenTelemetry logging for Production
        exporter = OTLPLogExporter(
            endpoint=config.OPEN_TELEMETRY_ENDPOINT,
            headers={"Authorization": config.OPEN_TELEMETRY_AUTHORIZATION_TOKEN},
        )
        processor = BatchLogRecordProcessor(exporter)
        logger_provider.add_log_record_processor(processor)

        handlers = {
            "default": {
                "class": "rich.logging.RichHandler",
                "level": config.LOG_LEVEL,
                "formatter": "console",
                "show_path": False,
            },
            "otel": {
                "()": LoggingHandler,
                "level": config.LOG_LEVEL,
                "logger_provider": logger_provider,
            },
        }
    else:
        handlers = {
            "default": {
                "class": "rich.logging.RichHandler",
                "level": config.LOG_LEVEL,
                "formatter": "console",
                "show_path": False,
            },
        }

    formatters = {
        "console": {
            "class": "logging.Formatter",
            "datefmt": "%Y-%m-%dT%H:%M:%S",
            "format": "%(name)s:%(lineno)d - %(message)s",
        }
    }

    # Declare src logger as the root logger
    # Any other loggers will be children of src and inherit the settings
    loggers = {
        "src": {
            "level": config.LOG_LEVEL,
            "handlers": list(handlers.keys()),
            "propagate": False,
        }
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
