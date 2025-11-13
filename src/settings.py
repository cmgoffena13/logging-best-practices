from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Store all environment variables that can be accessed globally
class GlobalConfig(BaseConfig):
    LOG_LEVEL: str = "INFO"


class DevConfig(GlobalConfig):
    LOG_LEVEL: str = "DEBUG"  # Overrides the global LOG_LEVEL

    model_config = SettingsConfigDict(env_prefix="DEV_")


class TestConfig(GlobalConfig):
    LOG_LEVEL: str = "DEBUG"

    model_config = SettingsConfigDict(env_prefix="TEST_")


class ProdConfig(GlobalConfig):
    LOG_LEVEL: str = "WARNING"

    model_config = SettingsConfigDict(env_prefix="PROD_")


@lru_cache()
def get_config(env_state: str):
    if not env_state:
        raise ValueError("ENV_STATE is not set. Possible values are: DEV, TEST, PROD")
    env_state = env_state.lower()
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
    return configs[env_state]()


config = get_config(BaseConfig().ENV_STATE)
