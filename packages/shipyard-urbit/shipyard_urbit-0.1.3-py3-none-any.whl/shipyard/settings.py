from typing import Optional
from pydantic import BaseSettings, PostgresDsn
from pathlib import Path

DEFAULT_DATA_DIR = Path.home() / ".shipyard"
DEFAULT_SQLITE_FILENAME = Path("shipyard.db")


class Settings(BaseSettings):
    data_dir: Path = DEFAULT_DATA_DIR
    sqlite_filename: Path = DEFAULT_SQLITE_FILENAME
    postgres_url: Optional[PostgresDsn] = None

    class Config:
        env_prefix = "shipyard_"
        env_file = ".env"


_settings: Optional[Settings] = None


def load_settings(**kwargs) -> Settings:
    global _settings
    if _settings:
        raise Exception("Settings must be loaded only once.")
    else:
        _settings = Settings(**kwargs)
    return _settings


def get_settings() -> Settings:
    global _settings
    if not _settings:
        raise Exception("Settings must be loaded before being used.")
    return _settings
