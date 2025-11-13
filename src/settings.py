from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Store all environment variables that can be accessed globally
class GlobalConfig(BaseConfig):
    LOG_LEVEL: str = "INFO"
    OTEL_PYTHON_LOG_CORRELATION: Optional[bool] = None
    OPEN_TELEMETRY_ENDPOINT: Optional[str] = None
    OPEN_TELEMETRY_AUTHORIZATION_TOKEN: Optional[str] = None


class DevConfig(GlobalConfig):
    LOG_LEVEL: str = "DEBUG"  # Overrides the global LOG_LEVEL
    OTEL_PYTHON_LOG_CORRELATION: bool = False

    model_config = SettingsConfigDict(env_prefix="DEV_")


class TestConfig(GlobalConfig):
    LOG_LEVEL: str = "DEBUG"
    OTEL_PYTHON_LOG_CORRELATION: bool = False

    model_config = SettingsConfigDict(env_prefix="TEST_")


class ProdConfig(GlobalConfig):
    LOG_LEVEL: str = "WARNING"
    OTEL_PYTHON_LOG_CORRELATION: bool = True

    model_config = SettingsConfigDict(env_prefix="PROD_")


@lru_cache()
def get_config(env_state: str):
    if not env_state:
        raise ValueError("ENV_STATE is not set. Possible values are: DEV, TEST, PROD")
    env_state = env_state.lower()
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
    return configs[env_state]()


config = get_config(BaseConfig().ENV_STATE)
