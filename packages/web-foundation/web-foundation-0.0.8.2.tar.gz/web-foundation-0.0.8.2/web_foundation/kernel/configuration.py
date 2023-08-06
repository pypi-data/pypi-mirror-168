from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel, BaseSettings


class ServerConfig(BaseModel):
    host: str
    port: int


class DbConfig(BaseModel):
    host: str
    port: str
    database: str
    user: str
    password: str
    db_schema: str
    with_migrations: bool
    migrations_path: Path


class AppConf(BaseSettings):
    app_name: str
    server: ServerConfig
    database: DbConfig


GenericConfig = TypeVar("GenericConfig", bound=BaseSettings)
