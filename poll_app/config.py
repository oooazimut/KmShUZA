from pathlib import Path

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent


class ModbusSettings(BaseModel):
    host: str
    port: int
    address: int
    count: int


class PGSettings(BaseModel):
    host: str
    port: int
    db_name: str
    user: str
    passw: SecretStr


class Settings(BaseSettings):
    sqlite_db_path: Path = BASE_DIR / "infra/repo/sqlite/db.sqlite"
    modbus: ModbusSettings
    pg: PGSettings

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


settings = Settings()
