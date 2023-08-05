"""Declares :class:`Action`."""
from email.policy import default
import inspect
import types
import typing
from typing import Any
from typing import Callable
from typing import TypeAlias

import pydantic
from cbra.headers import HEADERS_RESPONSE_BODY
from cbra.headers import CORS_HEADERS
from cbra.headers import DIGEST_SCHEMA
from cbra.types import IEndpoint
from .iresource import IResource
from .pathparameter import PathParameter
from .resourceoptions import ResourceOptions


ModelType: TypeAlias = type[pydantic.BaseModel] | types.UnionType


class Action:
    __module__: str = 'cbra.resource'
    summary = {
        'create'    : "Create {article} {name}",
        'retrieve'  : "Retrieve {article} {name}",
        'update'    : "Update (patch) {article} {name}",
        'replace'   : "Replace {article} {name}",
        'delete'    : "Delete {article} {name}",
        'list'      : "List {pluralname}",
        'purge'     : "Delete all {pluralname}",
    }
    default_actions: typing.Dict[str, typing.Tuple[str, bool]] = {
        'create'    : ('POST', False),
        'list'      : ('GET', False),
        'purge'     : ('DELETE', False),
        'retrieve'  : ('GET', True),
        'update'    : ('PATCH', True),
        'replace'   : ('PUT', True),
        'delete'    : ('DELETE', True),
    }
    is_detail: bool
    name: str
    method: str
    path_parameter: PathParameter
    response_descriptions: typing.Dict[str, str] = {
        'create'    : "The created **{name}** object or a reference to its location.",
        'retrieve'  : "The **{name}** object specified by the path parameter(s).",
        'purge'     : "The list of deleted **{name}** objects.",
        'delete'    : "The deleted **{name}** object specified by the path parameter(s).",
        'list'      : "The list of **{pluralname}** objects matching the search criterion.",
        'update'    : "The updated **{name}** object specified by the path parameter(s).",
        'replace'   : "The replaced **{name}** object specified by the path parameter(s).",
    }
    subpath: typing.Optional[str]
    queryable_methods = {"GET", "DELETE"}

    @staticmethod
    def creates_resource(action: str) -> bool:
        return action == "create"

    @staticmethod
    def model_from_signature(func: Callable[..., Any]) -> ModelType | None:
        sig = inspect.signature(func)
        args = list(sig.parameters.values())
        if len(args) == 1: # No request body model
            return None
        model: None | ModelType = None
        if inspect.isclass(args[1].annotation)\
        and issubclass(args[1].annotation, (pydantic.BaseModel, types.UnionType)):
            model = args[1].annotation # type: ignore
        return model

    @classmethod
    def fromclass(
        cls,
        resource_class: typing.Type[IResource]
    ) -> typing.Generator['Action', None, None]:

        path_parameter = typing.cast(PathParameter, resource_class.path_parameter)
        detail_methods: typing.Set[str] = set()
        list_methods: typing.Set[str] = set()
        for attname, member in inspect.getmembers(resource_class):
            if attname not in cls.default_actions\
            and (not hasattr(member, 'action') or not inspect.isfunction(member)):
                continue
            if hasattr(member, 'action'):
                action_name = member.action.pop('name')
                handler: typing.Type[IEndpoint] = resource_class.new(
                    action=action_name,
                    cors_policy=resource_class.cors_policy,
                    handle=member,
                    method="POST",
                    model=cls.model_from_signature(member),
                    name=resource_class.name,
                    **member.action
                )
                action = Action(
                    name=action_name,
                    handler=typing.cast(typing.Type[IResource], handler),
                    method=handler.method,
                    is_detail=True,
                    path_parameter=path_parameter
                )
                yield action
                yield action.as_options(
                    summary=member.action.get('summary') or action_name,
                    methods=["POST"],
                    name=action_name,
                    subpath=action_name
                )
                continue
            if attname in cls.default_actions:
                method, is_detail = cls.default_actions[attname]
                response_description = cls.response_descriptions.get(attname, "Success")\
                    .format(
                        article=resource_class.name_article,
                        name=resource_class.verbose_name,
                        pluralname=resource_class.verbose_name_plural
                    )


                # Hack: determine some parameter if there is no response.
                response_model = resource_class.model
                default_response_code = 201 if cls.creates_resource(attname) else 200
                if inspect.signature(member).return_annotation is None:
                    default_response_code = 204
                handler: typing.Type[IEndpoint] = resource_class.new(
                    action=attname,
                    cors_policy=resource_class.cors_policy,
                    default_response_code=default_response_code,
                    handle=member,
                    is_detail=is_detail,
                    method=method,
                    model=response_model,
                    name=resource_class.name,
                    queryable=not is_detail and method in cls.queryable_methods,
                    response_description=getattr(member, 'response_description', response_description),
                    searchable=attname in resource_class.filter_actions,
                    summary=getattr(member, "summary", None)
                )
                yield Action(
                    name=attname,
                    handler=typing.cast(typing.Type[IResource], handler),
                    method=method,
                    is_detail=is_detail,
                    path_parameter=path_parameter
                )
                detail_methods.add(method)\
                    if is_detail else\
                    list_methods.add(method)

        if list_methods:
            yield Action(
                name='options',
                path_parameter=path_parameter,
                method='OPTIONS',
                handler=typing.cast(
                    typing.Type[IResource],
                    ResourceOptions.new(
                        allowed_methods=list_methods,
                        cors_policy=resource_class.cors_policy,
                        document=resource_class.document,
                        is_detail=False,
                        model=resource_class.model,
                        path_parameters=resource_class.get_path_signature(False),
                        name=resource_class.name,
                        pluralname=resource_class.pluralname,
                        summary="Collection endpoint options and CORS policy",
                        verbose_name=resource_class.verbose_name,
                        verbose_name_plural=resource_class.verbose_name_plural
                    )
                ),
                is_detail=False
            )

        if detail_methods:
            assert path_parameter.signature_parameter is not None # nosec
            yield Action(
                name='options',
                path_parameter=path_parameter,
                method='OPTIONS',
                handler=typing.cast(
                    typing.Type[IResource],
                    ResourceOptions.new(
                        allowed_methods=detail_methods,
                        cors_policy=resource_class.cors_policy,
                        document=resource_class.document,
                        is_detail=True,
                        model=resource_class.model,
                        path_parameters=resource_class.get_path_signature(True),
                        name=resource_class.name,
                        pluralname=resource_class.pluralname,
                        summary="Detail endpoint options and CORS policy",
                        verbose_name=resource_class.verbose_name,
                        verbose_name_plural=resource_class.verbose_name_plural
                    )
                ),
                is_detail=True
            )

    def __init__(
        self,
        *,
        name: str,
        handler: typing.Type[IResource],
        method: str,
        is_detail: bool,
        path_parameter: PathParameter,
        subpath: typing.Optional[str] = None,
    ):
        self.name = name
        self.handler = handler
        self.method = method
        self.is_detail = is_detail
        self.subpath = subpath
        self.path_parameter = path_parameter

    def as_options(
        self,
        *,
        summary: str,
        methods: list[str],
        name: str = 'options',
        subpath: str | None = None,
    ) -> 'Action':
        """Return the options action for this action."""
        cls = self.handler
        return Action(
            name=name,
            path_parameter=self.path_parameter,
            method='OPTIONS',
            handler=typing.cast(
                typing.Type[IResource],
                ResourceOptions.new(
                    allowed_methods=methods,
                    cors_policy=cls.cors_policy,
                    document=cls.document,
                    is_detail=self.is_detail,
                    path_parameters=cls.get_path_signature(self.is_detail),
                    name=cls.name,
                    pluralname=cls.pluralname,
                    summary=summary,
                    verbose_name=cls.verbose_name,
                    verbose_name_plural=cls.verbose_name_plural
                )
            ),
            is_detail=self.is_detail,
            subpath=subpath
        )

    def add_to_router(
        self,
        app: IEndpoint.RouterType,
        base_path: str
    ) -> None:
        path = base_path if not self.is_detail else f'{base_path}/{{id}}'
        subpath = None
        if (self.name not in self.default_actions)\
        and (self.name != 'options'):
            # TODO: Find a cleaner way to construct the path.
            subpath = self.subpath or self.name

        path = self.path_parameter.get_path(
            base_path=base_path,
            subpath=subpath,
            is_detail=self.is_detail
        )
        self.handler.add_to_router(
            app=app,
            base_path=path,
            method=self.method,
            request_handler=...,
            **self.get_app_parameters(self.handler)
        )

    def get_app_parameters(
        self,
        resource_class: typing.Type[IResource]
    ) -> typing.Dict[str, typing.Any]:
        params: typing.Dict[str, typing.Any] = {
            'summary': resource_class.summary,
            'tags': [resource_class.verbose_name_plural],
            'openapi_extra': self.get_openapi_schema(resource_class)
        }
        if self.name != 'options':
            params['name'] = str.lower(f'{self.handler.name}.{self.name}')

        description = getattr(resource_class.handle, '__doc__', None)
        if description:
            params['description'] = description
        if self.name in self.summary and not resource_class.summary:
            params['summary'] = self.summary[self.name].format(
                article=resource_class.name_article,
                name=resource_class.verbose_name or str.title(resource_class.name),
                pluralname=resource_class.verbose_name_plural\
                    or str.title(resource_class.pluralname)
            )

        if self.name in self.response_descriptions:
            tpl = self.response_descriptions[self.name]
            params['response_description'] = tpl.format(
                article=resource_class.name_article,
                name=resource_class.verbose_name,
                pluralname=resource_class.verbose_name_plural
            )

        hints = typing.get_type_hints(resource_class.handle)
        returns = hints.get('return')
        origin = typing.get_origin(returns)
        if origin == list:
            params['response_model'] = returns
        elif inspect.isclass(returns) and issubclass(returns, (pydantic.BaseModel, types.UnionType)):
            params['response_model'] = returns

        return params

    def get_openapi_schema(
        self,
        resource_class: typing.Type[IResource]
    ) -> typing.Dict[str, typing.Any]:
        if self.name not in {"create", "update", "replace"}:
            return {}

        schema: typing.Dict[str, typing.Any] = {}
        models = typing.get_args(resource_class.model)
        oneOf: list[dict[str, typing.Any]] = []
        if models:
            schema['oneOf'] = oneOf
            for model in typing.get_args(models):
                if not inspect.isclass(model)\
                or not issubclass(model, pydantic.BaseModel):
                    raise TypeError(
                        f"{resource_class.__name__}.model must be a subclass of "
                        "pydantic.BaseModel or subclass thereof."
                    )
                oneOf.append(model.schema())
        elif inspect.isclass(resource_class.model)\
        and issubclass(resource_class.model, pydantic.BaseModel):
            schema = resource_class.model.schema()
        else:
            # TODO: Inspect the parameters for pydantic implementations.
            # This should also support plain annotations.
            sig = inspect.signature(self.handler.handle) # type: ignore
            params = sig.parameters
            models: list[type[pydantic.BaseModel]] = []
            for name, value in params.items():
                if name == 'self' or not inspect.isclass(value.annotation):
                    continue
                if not issubclass(value.annotation, pydantic.BaseModel):
                    continue
                models.append(value.annotation)
            if len(models) > 1:
                raise NotImplementedError("Discovery of multiple models is not implemented.")
            if models:
                schema = models[0].schema()
        return {
            'requestBody': {
                'content': {
                    p.media_type: {
                        'schema': schema
                    }
                    for p in resource_class.parsers
                    if schema
                }
            }
        }

    def get_response_description(
        self,
        resource_class: typing.Type[IResource],
        action: str
    ) -> str:
        return self.response_descriptions[self.name].format(
            article=resource_class.name_article,
            name=resource_class.name,
            pluralname=resource_class.pluralname
        )
