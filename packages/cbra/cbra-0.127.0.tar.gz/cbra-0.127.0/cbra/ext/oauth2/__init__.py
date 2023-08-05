# pylint: skip-file
import functools
from typing import Any
from typing import Callable

from cbra.exceptions import MissingScope
from cbra.resource import Resource
from . import exceptions
from . import params
from . import types
from .authorizeendpoint import AuthorizationEndpoint
from .authorizationserver import AuthorizationServer
from .authorizationrequestclient import AuthorizationRequestClient
from .clientconfig import ClientConfig
from .configfileclientrepository import ConfigFileClientRepository
from .introspectionendpoint import IntrospectionEndpoint
from .memorystorage import MemoryStorage
from .memoryclientrepository import MemoryClientRepository
from .memorysubjectrepository import MemorySubjectRepository
from .nullsubjectrepository import NullSubjectRepository
from .oidcclaimhandler import OIDCClaimHandler
from .oidctokenbuilder import OIDCTokenBuilder
from .pushedauthorizationrequestendpoint import PushedAuthorizationRequestEndpoint
from .rfc9068principal import RFC9068Principal
from .settingsclientrepository import SettingsClientRepository
from .settingssubjectrepository import SettingsSubjectRepository
from .staticsubjectepository import StaticSubjectRepository
from .tokenissuer import TokenIssuer
from .tokenrequesthandler import TokenRequestHandler
from .upstreamreturnhandler import UpstreamReturnHandler
from .upstreamprovider import UpstreamProvider


__all__: list[str] = [
    'exceptions',
    'params',
    'scope',
    'types',
    'AuthorizationEndpoint',
    'AuthorizationServer',
    'AuthorizationRequestClient',
    'ClientConfig',
    'ConfigFileClientRepository',
    'IntrospectionEndpoint',
    'MemoryClientRepository',
    'MemoryStorage',
    'MemorySubjectRepository',
    'NullSubjectRepository',
    'OIDCClaimHandler',
    'OIDCTokenBuilder',
    'PushedAuthorizationRequestEndpoint',
    'RFC9068Principal',
    'SettingsClientRepository',
    'SettingsSubjectRepository',
    'StaticSubjectRepository',
    'TokenIssuer',
    'TokenRequestHandler',
    'UpstreamReturnHandler',
    'UpstreamProvider',
]


def scope(required: str | set[str]) -> Callable[..., Any]:
    """Method decorator for :class:`~cbra.Resource` implementations
    that enforces a given scope.
    """
    if isinstance(required, str):
        required = {required}

    def decorator_factory(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        async def f(self: Resource, *args: Any, **kwargs: Any):
            assert isinstance(required, set) # nosec
            if not self.principal.has_scope(required):
                missing: set[str] = required - self.principal.get_current_scope()
                raise MissingScope(missing=missing)
            return await func(self, *args, **kwargs)
        return f
    return decorator_factory