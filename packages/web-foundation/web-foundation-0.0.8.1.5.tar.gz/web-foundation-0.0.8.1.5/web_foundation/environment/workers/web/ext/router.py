from dataclasses import dataclass
from typing import Dict, Any
from typing import List, Type, Callable, Generic

from pydantic import BaseModel
from sanic import Sanic, HTTPResponse
from sanic.router import Router

from web_foundation.environment.workers.web.ext.addons_loader import AddonsLoader
from web_foundation.environment.workers.web.ext.request_handler import HandlerType, Protector, GenericRequestHandler
from web_foundation.environment.workers.web.utils.openapi_spec import add_openapi_spec
from web_foundation.kernel.abstract.container import GenericDepContainer


@dataclass
class RouteMethodConf:
    method_name: str
    protector: Protector | None
    in_dto: Type[BaseModel] | None
    out_dto: Type[BaseModel] | None
    handler: HandlerType
    response_fabric: Callable[[Any], HTTPResponse] | None
    version_prefix: str | None
    version: str | None


@dataclass
class RouteConf:
    app_name: str
    path: str
    methods: List[RouteMethodConf]


class ExtRouter(Router, Generic[GenericRequestHandler]):
    ext_handler: GenericRequestHandler
    parsed_routes: List[RouteConf]

    def __init__(self, ext_handler: GenericRequestHandler):
        super().__init__()
        self.ext_handler = ext_handler
        self.parsed_routes = []

    def apply_routes(self, app: Sanic, container: GenericDepContainer, *args, **kwargs):
        raise NotImplementedError


class DictRouter(ExtRouter, Generic[GenericRequestHandler]):
    _router_conf: Dict
    addon_loader: AddonsLoader | None
    versioning: bool
    open_api: bool

    def __init__(self,
                 routes_config: Dict,
                 ext_handler: GenericRequestHandler,
                 versioning: bool = True,
                 open_api: bool = True):
        super().__init__(ext_handler)
        self._router_conf = routes_config
        self.versioning = versioning
        self.open_api = open_api
        self._parse()

    def _parse(self):
        for app_route in self._router_conf.get("apps"):
            version_prefix = app_route.get("version_prefix")
            version_prefix = version_prefix if version_prefix else "/api/v"
            for endpoint, versions in app_route.get("endpoints").items():
                for version, params in versions.items():
                    methods_confs = []
                    endpoint_handler = params.pop("handler", None)
                    endpoint_protector = params.pop("protector", None)
                    endpoint_response_fabric = params.pop("response_fabric", None)
                    for method_name, method_params in params.items():
                        target_func = method_params.get('handler')
                        target_func = target_func if target_func else endpoint_handler
                        protector = method_params.get("protector")
                        protector = protector if protector else endpoint_protector
                        in_dto = method_params.get("in_dto")
                        out_dto = method_params.get("out_dto")
                        response_fabric = method_params.get("response_fabric")
                        response_fabric = response_fabric if response_fabric else endpoint_response_fabric

                        methods_confs.append(RouteMethodConf(method_name=method_name,
                                                             protector=protector,
                                                             in_dto=in_dto,
                                                             out_dto=out_dto,
                                                             handler=target_func,
                                                             response_fabric=response_fabric,
                                                             version_prefix=version_prefix,
                                                             version=version
                                                             ))

                    route = RouteConf(app_name=app_route.get("app_name"),
                                      path=endpoint,
                                      methods=methods_confs)
                    self.parsed_routes.append(route)

    def apply_routes(self, app: Sanic, container: GenericDepContainer = None, addon_manager: AddonsLoader = None,
                     **kwargs):
        for route_conf in self.parsed_routes:
            for method_conf in route_conf.methods:
                if method_conf.response_fabric:
                    chain = self.ext_handler(protector=method_conf.protector,
                                             in_struct=method_conf.in_dto,
                                             addon_manager=addon_manager,
                                             response_fabric=method_conf.response_fabric,
                                             container=container)(method_conf.handler)
                else:
                    chain = self.ext_handler(protector=method_conf.protector,
                                             addon_manager=addon_manager,
                                             in_struct=method_conf.in_dto,
                                             container=container)(method_conf.handler)
                if self.open_api:
                    chain = add_openapi_spec(uri=route_conf.path,
                                             method_name=method_conf.method_name,
                                             func=method_conf.handler,
                                             handler=chain,
                                             in_dto=method_conf.in_dto,
                                             out_dto=method_conf.out_dto)

                if self.versioning:
                    app.add_route(uri=route_conf.path,
                                  methods={method_conf.method_name.upper()},
                                  handler=chain,
                                  version_prefix=method_conf.version_prefix,
                                  version=method_conf.version)
                else:
                    app.add_route(uri=route_conf.path,
                                  methods={method_conf.method_name.upper()},
                                  handler=chain)

        # warn(f"Can't find dto or handler in imported module, suppressed exception: {e.__str__()}")
