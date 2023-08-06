import importlib
import os
from typing import List, Generic

from loguru import logger
from tortoise import Tortoise, BaseDBAsyncClient, connections

from web_foundation.kernel.abstract.resource import Resource
from web_foundation.kernel.configuration import DbConfig
from web_foundation.kernel.configuration import GenericConfig


class DatabaseResource(Resource, Generic[GenericConfig]):
    connection: BaseDBAsyncClient | None
    _app_name: str
    _modules: List[str]
    _engine: str
    db_conf: DbConfig

    def __init__(self, modules: List[str], engine: str = 'tortoise.backends.asyncpg'):
        self._engine = engine
        self._modules = modules

    def _get_connection_setting(self) -> dict:
        if self.db_conf.with_migrations and "aerich.models" not in self._modules:
            self._modules.append("aerich.models")
        to_discover = [importlib.import_module(i) for i in self._modules]
        return {
            'connections': {
                # Dict format for connection
                f'{self._app_name}_default': {
                    'engine': self._engine,
                    'credentials': {
                        'host': self.db_conf.host,
                        'port': self.db_conf.port,
                        'user': self.db_conf.user,
                        'password': self.db_conf.password,
                        'database': self.db_conf.database,
                        'schema': self.db_conf.db_schema,
                        'minsize': 1,
                        'maxsize': 5,
                    }
                }
            },
            'apps': {
                f'{self._app_name}': {
                    'models': to_discover,
                    'default_connection': f'{self._app_name}_default',
                }
            },
            'use_tz': False,
            'timezone': 'UTC'
        }

    async def fill_db_data(self):
        pass

    async def init(self, config: GenericConfig, **kwargs) -> BaseDBAsyncClient:
        self._app_name = config.app_name
        self.db_conf = config.database
        self.connection = None
        await Tortoise.init(config=self._get_connection_setting())
        await self.configure_db()
        return Tortoise.get_connection(f'{self._app_name}_default')

    async def shutdown(self) -> None:
        await connections.close_all()

    @property
    def conn(self) -> BaseDBAsyncClient:
        if not self.connection:
            self.connection = Tortoise.get_connection(connection_name=f'{self._app_name}_default')
        return self.connection

    async def _migrations(self, schema_exists: bool, command):
        path_exists = os.path.exists(os.path.join(os.getcwd(), self.db_conf.migrations_path)) and os.listdir(
            os.path.join(os.getcwd(), self.db_conf.migrations_path))

        if not path_exists and not schema_exists:
            await self.create_schema(False)
            await command.init()
            await command.init_db(safe=True)
        elif not schema_exists:
            await self.create_schema(False)
            await command.init()
            await command.upgrade()
        elif not path_exists:
            await command.init()
            await command.init_db(safe=True)  # TODO check - need to drop aerich table in db?
        await command.init()
        logger.info(f"Apply migrations from {self.db_conf.migrations_path}")
        await command.migrate()
        await command.upgrade()

    async def configure_db(self):
        scheme_name = self.db_conf.db_schema
        row_count, rows = await self.conn.execute_query(
            "SELECT schema_name FROM information_schema.schemata WHERE schema_name = $1", [scheme_name])
        schema_exists = True if row_count else False
        if self.db_conf.with_migrations:
            if not self.db_conf.migrations_path:
                raise ValueError("Migration Path not set can't migrate")
            try:
                from aerich import Command
            except ImportError:
                raise ImportError("To use migration need to install aerich, (web-foundation[aerich])")
            command = Command(tortoise_config=self._get_connection_setting(), app=self._app_name,
                              location=self.db_conf.migrations_path)
            await self._migrations(schema_exists, command)
        if not schema_exists:
            await self.create_schema()
            await self.fill_db_data()

    async def create_schema(self, generate_schemas: bool = True):
        await self.conn.execute_script(f"CREATE SCHEMA IF NOT EXISTS {self.db_conf.db_schema};")
        if generate_schemas:
            await Tortoise.generate_schemas()
