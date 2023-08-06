from abc import ABC
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, Type, Coroutine, TypeVar, Generic
from typing import Dict

from pydantic import BaseModel as PdModel
from sanic import Request, json, HTTPResponse

from web_foundation.environment.container import GenericAppDepContainer
from web_foundation.environment.workers.web.ext.addons_loader import AddonsLoader
from web_foundation.kernel.abstract.container import GenericDepContainer
from web_foundation.utils.validation import validate_dto

DtoType = TypeVar("DtoType", bound=PdModel)


@dataclass
class ProtectIdentity:
    pass


ProtectIdentityType = TypeVar("ProtectIdentityType", bound=ProtectIdentity)


@dataclass
class InputContext(Generic[DtoType, ProtectIdentityType]):
    request: Request
    dto: DtoType | None
    identity: ProtectIdentity | None
    r_kwargs: Dict


Protector = Callable[[Request, GenericAppDepContainer], Coroutine[Any, Any, ProtectIdentityType | None]]
DtoValidator = Callable[[Type[DtoType], Request], PdModel]
HandlerType = Callable[[InputContext, GenericAppDepContainer], Coroutine[Any, Any, HTTPResponse]]


class ExtRequestHandler(ABC, Generic[GenericAppDepContainer]):
    protector: Protector | None
    in_struct: Type[PdModel] | None
    addons_loader: AddonsLoader | None
    validation_fnc: DtoValidator | None
    container: GenericAppDepContainer | None
    response_fabric: Callable[[Any], HTTPResponse] | None

    def __init__(self,
                 container: GenericDepContainer = None,
                 protector: Protector = None,
                 in_struct: Type[PdModel] | None = None,
                 addon_manager: AddonsLoader = None,
                 validation_fnc: DtoValidator = validate_dto,
                 response_fabric: Callable[[Any], HTTPResponse] = json):
        self.protector = protector
        self.in_struct = in_struct
        self.addons_loader = addon_manager
        self.validation_fnc = validation_fnc
        self.response_fabric = response_fabric
        self.container = container

    def __call__(self, target: HandlerType):
        raise NotImplementedError


GenericRequestHandler = TypeVar('GenericRequestHandler', bound=ExtRequestHandler)


class ChainRequestHandler(ExtRequestHandler, Generic[GenericAppDepContainer]):

    def __call__(self, target: HandlerType):
        @wraps(target)
        async def f(*args, **kwargs):
            req: Request = args[0]
            prot_identity = await self.protector(req, self.container) if self.protector else None
            if self.in_struct:
                validated = self.validation_fnc(self.in_struct, req)
            else:
                validated = None
            incoming = InputContext(req, validated, prot_identity, kwargs)
            if self.addons_loader:
                plugins = await self.addons_loader.find_middleware_by_target(target.__name__)
                for plugin in await self.addons_loader.find_middleware_by_target(target.__name__):
                    await plugin.exec_before(context=incoming, container=self.container)
                if not plugins:
                    ret_val = await target(incoming, self.container)
                else:
                    overrides = [pl for pl in plugins if pl.override]
                    if overrides:
                        ret_val = await overrides[0].exec_override(context=incoming, container=self.container)
                    else:
                        ret_val = await target(incoming, self.container)
                    for plugin in plugins:
                        await plugin.exec_after(context=incoming, container=self.container, target_result=ret_val)
            else:
                ret_val = await target(incoming, self.container)
            return self.response_fabric(ret_val)

        return f


"""
def chain(protector: Protector = None,
          in_struct: Type[PdModel] | None = None,
          plugin_manager: AddonsLoader = None,
          validation_fnc: DtoValidator = validate_dto,
          response_fabric: Callable[[TypeJSON], HTTPResponse] = json,
          container: Container = None
          ):
    def called_method(target: HandlerType):
        @wraps(target)
        async def f(*args, **kwargs):
            req: Request = args[0]
            prot_identity = await protector(req) if protector else None
            if in_struct:
                validated = validation_fnc(in_struct, req)
            else:
                validated = None
            incoming = InputContext(req, validated, prot_identity, kwargs)
            if plugin_manager:
                plugins = await plugin_manager.find_middleware_by_target(target.__name__)
                for plugin in await plugin_manager.find_middleware_by_target(target.__name__):
                    await plugin.exec_before(context=incoming, container=container)
                if not plugins:
                    ret_val = await target(incoming, container)
                else:
                    overrides = [pl for pl in plugins if pl.override]
                    if overrides:
                        ret_val = await overrides[0].exec_override(context=incoming, container=container)
                    else:
                        ret_val = await target(incoming, container)
                    for plugin in plugins:
                        await plugin.exec_after(context=incoming, container=container, target_result=ret_val)
            else:
                ret_val = await target(incoming, container)
            return response_fabric(ret_val)

        return f

    return called_method
"""
