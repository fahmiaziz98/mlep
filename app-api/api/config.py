import sys
import enum
import logging
from functools import lru_cache
from types import FrameType
from typing import List, Optional, cast
from pydantic import AnyHttpUrl, BaseSettings


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """ Possible log levels """

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"

class Settings(BaseSettings):
    """
    Pengaturan aplikasi.

    Parameter ini dapat dikonfigurasi
    dengan variabel lingkungan.
    """

    # Konfigurasi Umum
    HOST: str = "0.0.0.0"
    PORT: int = 8001
    LOG_LEVEL: LogLevel = LogLevel.INFO
    # Versi api sekarang
    VERSION: str = "v1"
    # Jumlah pekerja untuk uvicorn.
    WORKERS_COUNT: int = 1
    # Mengaktifkan pemuatan ulang uvicorn.
    RELOAD: bool = False
    PROJECT_NAME: str = "ENERGY CONSUMPTION API"

    # GCP Credentials
    GCP_PROJECT: Optional[str] = None
    GCP_BUCKET: Optional[str] = None 
    GCP_SERVICE_ACCOUNT_JSON_PATH: Optional[str] = None
        
    class Config:
        env_file = ".env.default"
        env_prefix = "APP_API_"
        case_sensitive = False
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings():
    return Settings()