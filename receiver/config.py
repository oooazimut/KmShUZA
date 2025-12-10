from pydantic import BaseModel
from pydantic_settings import BaseSettings


class ModbusSettings(BaseModel):
    host: str
    port: int
    address: int
    count: int


class Settings(BaseSettings):
    # db_path: Path = BASE_DIR / "infra/repo/sqlite/db.sqlite"
    modbus: ModbusSettings
    # pg: PGSettings

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


settings = Settings()
