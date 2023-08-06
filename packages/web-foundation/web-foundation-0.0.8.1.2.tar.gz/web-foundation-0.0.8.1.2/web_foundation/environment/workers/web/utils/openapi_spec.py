import inspect
import re
from copy import deepcopy
from typing import Dict, Callable, Type

import sanic_ext
from pydantic import BaseModel as PdModel
from sanic_ext.extensions.openapi.builders import SpecificationBuilder, OperationStore


def get_definition_with_correct_name(definitions: Dict) -> Dict:
    _definitions = {}
    for defin, _schema in definitions.copy().items():
        if "." in defin:
            _definitions[defin.split(".")[-2]] = _schema
        else:
            _definitions[defin] = _schema
    return _definitions


def get_model_schema(model: Type[PdModel]):
    """ Create schema from pydantic model and add all references to OpenAPI schemas """
    schema = model.schema(ref_template="#/components/schemas/{model}")
    components = {}
    if "definitions" in schema:
        definitions = get_definition_with_correct_name(schema.pop("definitions"))
        components.update(definitions)
    components.update({model.__name__: schema})
    spec = SpecificationBuilder()
    for component_name, component in components.items():
        spec._components["schemas"].update({component_name: component})
    return schema


def add_openapi_spec(uri: str, method_name: str, func: Callable, handler: Callable,
                     in_dto: Type[PdModel] | None, out_dto: Type[PdModel] | None):
    # --- copy existed openapi params ---#
    if OperationStore().get(func):
        OperationStore()[handler] = deepcopy(OperationStore().get(func))
    # --- add query args ---#
    func_text = inspect.getsource(func)
    func_query_args = set(re.findall(r"request.args.get\(\"(\w*)\"\)", func_text))
    if func_query_args:
        for func_arg in func_query_args:
            handler = sanic_ext.openapi.parameter(func_arg)(handler)
    # --- add request body ---#
    if in_dto:
        if issubclass(in_dto, PdModel):
            schema = get_model_schema(in_dto)
            if not hasattr(OperationStore()[handler], "requestBody"):
                OperationStore()[handler].requestBody = {"content": {
                    "environment/json": {'schema': schema},
                    "multipart/form-data": {'schema': schema}
                }}
            elif not OperationStore()[handler].requestBody.get("content"):
                OperationStore()[handler].requestBody['content'] = {
                    "environment/json": {'schema': schema},
                    "multipart/form-data": {'schema': schema}
                }
            if not OperationStore()[handler].requestBody['content'].get("environment/json"):
                OperationStore()[handler].requestBody['content'].update({"environment/json": {'schema': schema}})
            elif not OperationStore()[handler].requestBody['content']["environment/json"].get("schema"):
                OperationStore()[handler].requestBody['content']["environment/json"].update({'schema': schema})
            else:
                for k, v in schema.items():
                    if isinstance(v, dict):
                        OperationStore()[handler].requestBody['content']["environment/json"]['schema'][k].update(v)
                    else:
                        OperationStore()[handler].requestBody['content']["environment/json"]['schema'][k] = v
            if not OperationStore()[handler].requestBody['content'].get("multipart/form-data"):
                OperationStore()[handler].requestBody['content'].update({"multipart/form-data": {'schema': schema}})
            elif not OperationStore()[handler].requestBody['content']["multipart/form-data"].get("schema"):
                OperationStore()[handler].requestBody['content']["multipart/form-data"].update({'schema': schema})
            else:
                for k, v in schema.items():
                    if isinstance(v, dict):
                        OperationStore()[handler].requestBody['content']["multipart/form-data"]['schema'][k].update(v)
                    else:
                        OperationStore()[handler].requestBody['content']["multipart/form-data"]['schema'][k] = v
    # --- add response ---#
    if out_dto:
        if issubclass(out_dto, PdModel):
            schema = get_model_schema(out_dto)
            existed_resp = OperationStore()[handler].responses.get("200")
            if not existed_resp:
                OperationStore()[handler].responses["200"] = {"content": {"environment/json": {'schema': schema}},
                                                              "description": "OK"}
            else:
                if not existed_resp.get('content'):
                    existed_resp.update({"content": {"environment/json": {'schema': schema}},
                                         "description": "OK"})
                elif not existed_resp['content'].get("environment/json"):
                    existed_resp['content'].update({"environment/json": {'schema': schema}})
                elif not existed_resp['content']["environment/json"].get("schema"):
                    existed_resp['content']["environment/json"].update({'schema': schema})
                else:
                    for k, v in schema.items():
                        if isinstance(v, dict):
                            existed_resp['content']["environment/json"]['schema'][k].update(v)
                        else:
                            existed_resp['content']["environment/json"]['schema'][k] = v
    # --- add tag ---#
    handler = sanic_ext.openapi.tag(uri.split("/")[1].capitalize())(handler)  # first path word

    # --- decription --- #
    # f = sanic_ext.openapi.description("hujkiikasdf;awerfl;jkasdfklj;asdfjkl;")(handler)
    # f = sanic_ext.openapi.summary("l;kasdjllww")(handler)

    # --- set operation id --- #
    handler = sanic_ext.openapi.operation(f"{method_name}~{uri}")(handler)
    return handler
