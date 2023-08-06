from __future__ import annotations
from __future__ import annotations

from importlib.abc import FileLoader
from importlib.util import module_from_spec
from importlib.util import spec_from_loader
from types import ModuleType
from typing import List

import loguru
from loguru import logger

from web_foundation import settings
from web_foundation.environment.events.store import StoreUpdateEvent
from web_foundation.environment.resources.file_repo.repo import FileRepository, AppFileSections, GenFileSections
from web_foundation.environment.resources.stores.store import AppStore

class ApiAddon:
    source: str
    imported: ModuleType | None

    target: str
    name: str
    filename: str
    enabled: bool = False

    before: bool = False
    override: bool = False
    after: bool = False

    def __init__(self, filename: str, source: str, name: str = None):
        self.name = name
        self.filename = filename
        self.source = source
        self.target = ""

    def import_it(self, spec):
        try:
            imported = module_from_spec(spec)
            spec.loader.exec_module(imported)
            self.imported = imported
            if hasattr(self.imported, "before"):
                self.before = True
            if hasattr(self.imported, "after"):
                self.after = True
            if hasattr(self.imported, "override"):
                self.override = True
        except Exception as e:
            self.enabled = False
            loguru.logger.error(f"Can't import plugin \"{self.name}\". Exception: {e}")

    def drop_imported(self):
        self.imported = None
        self.before = False
        self.override = False
        self.after = False

    async def exec_before(self, context, container):
        try:
            if self.before:
                await self.imported.before(context, container)
        except Exception as e:
            loguru.logger.error(f"Can't run plugin \"{self.name}\". Exception: {e}")

    async def exec_after(self, context, container, target_result):
        try:
            if self.after:
                await self.imported.after(context, container, target_result)
        except Exception as e:
            loguru.logger.error(f"Can't run plugin \"{self.name}\". Exception: {e}")

    async def exec_override(self, context, container):
        try:
            if self.override:
                return await self.imported.override(context, container)
        except Exception as e:
            loguru.logger.error(f"Can't run plugin \"{self.name}\". Exception: {e}")

    def __repr__(self):
        return f"ApiMiddleware({self.name} on {self.target})"

    def __eq__(self, other: ApiAddon):
        return self.name == other.name


class SourceCodeLoader(FileLoader):
    def __init__(self, fullname: str, source):
        super().__init__(fullname, source)
        self.path = source

    def get_source(self, fullname: str) -> str | bytes:
        return self.path


class AddonsLoader:
    repo: FileRepository = None
    store: AppStore = None
    sections: GenFileSections

    def __init__(self, sections: GenFileSections = AppFileSections):
        self.sections = sections

    async def _import_middleware(self, pl: ApiAddon):
        middlewares = await self.store.get_item("middleware") if await self.store.get_item("middleware") else []
        try:
            spec = spec_from_loader(pl.name, loader=SourceCodeLoader(pl.name, pl.source))
            pl.import_it(spec)
            if pl not in middlewares:
                middlewares.append(pl)
            await self.store.set_item("middleware", middlewares, send_event=False)
        except Exception as e:
            if settings.DEBUG:
                logger.debug(f"Can't load plugin {pl.name}, cause {str(e)}")

    async def import_middleware(self):
        middlewares = await self.store.get_item("middleware") if await self.store.get_item("middleware") else []
        for pl in middlewares:
            await self._import_middleware(pl)

    async def configure_middleware(self, plugin: ApiAddon, *args, **kwargs) -> ApiAddon:
        """Set middleware name, target and enabled"""
        raise NotImplementedError

    async def _discover_middleware(self, filename) -> ApiAddon | None:
        async with (await self.repo.take(filename, self.sections.PLUGINS)) as file_:
            pl = ApiAddon(filename, await file_.read())
            pl = await self.configure_middleware(pl)
            if pl.name is None:
                raise AttributeError("ApiMiddleware name must be specified")

            middlewares = await self.store.get_item("middleware") if await self.store.get_item("middleware") else []
            if middlewares and pl in middlewares:
                middlewares.remove(pl)
            middlewares.append(pl)
            await self.store.set_item("middleware", middlewares, obj=True)
            return pl

    async def discover_middleware(self):
        for filename in await self.repo.open_section(self.sections.PLUGINS):
            await self._discover_middleware(filename)

    async def delete_middleware(self, filename: str):
        mdws = await self.store.get_item("middleware")
        new_mdws: List[ApiAddon] = []
        for mdw in mdws:
            if mdw.filename != filename:
                new_mdws.append(mdw)
        await self.store.set_item("middleware", new_mdws, obj=True)
        await self.import_middleware()

    async def add_new_middleware(self, filename: str):
        pl = await self._discover_middleware(filename)
        if pl:
            await self._import_middleware(pl)
            if settings.DEBUG:
                logger.debug(f"New plugin added {pl}")

    async def find_middleware_by_target(self, target: str) -> List[ApiAddon]:
        middlewares = await self.store.get_item("middleware")
        if not middlewares:
            return []
        else:
            cell_plugins: List[ApiAddon] = []
            for pl in middlewares:
                if pl.target == target and pl.enabled:
                    cell_plugins.append(pl)
            return cell_plugins

    async def on_store_update(self, event: StoreUpdateEvent):
        if event.key == "middleware":
            await self.store.set_item("middleware", event.value, send_event=False)
            await self.import_middleware()

    def reg_channel_middleware(self):
        self.store.channel.add_event_middleware(StoreUpdateEvent.message_type, self.on_store_update)
        self.store.channel.add_event_middleware(StoreUpdateEvent.message_type, self.on_mdw_store_set,
                                                assign_to="before")

    async def on_mdw_store_set(self, event: StoreUpdateEvent):
        if event.key == "middleware":
            for mdw in event.value:
                mdw.imported = None

    async def first_init(self):
        await self.discover_middleware()
        await self.import_middleware()
