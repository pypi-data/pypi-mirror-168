# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio.exceptions
import functools
import logging
import ssl
from typing import Any
from typing import Callable

import fastapi
import httpcore
import httpx
from httpx import AsyncClient
from httpx import Response
from ckms.types import AuthorizationServerNotDiscoverable
from ckms.types import AuthorizationServerMisbehaves
from ckms.types import JSONWebKeySet
from ckms.types import ServerMetadata

from cbra.conf import settings
from cbra.exceptions import UpstreamServiceNotAvailable
from cbra.ext.oauth2.types import IntrospectionResponse
from cbra.ext.oauth2.types import TokenResponse
from cbra.utils import retry
from .credential import Credential
from .personaldatahandler import PersonalDataHandler
from .resource import Resource
from .serviceidentity import ServiceIdentity


RESOURCE_SERVERS: dict[str, Any] = getattr(settings, 'RESOURCE_SERVERS', {})


UpstreamFailure: UpstreamServiceNotAvailable = UpstreamServiceNotAvailable(5)
Retryables: list[type[BaseException]] = [
    asyncio.exceptions.CancelledError,
    httpx.ConnectTimeout,
    httpx.ReadTimeout,
    httpcore.ConnectTimeout,
    httpcore.ReadTimeout,
    ssl.SSLWantReadError
]


class ServiceClient:
    __module__: str = 'cbra.ext.service'
    credential: Credential | None
    encrypter: PersonalDataHandler
    http: AsyncClient
    identity: ServiceIdentity
    jwks: JSONWebKeySet | None
    logger: logging.Logger
    metadata: ServerMetadata
    server: str
    timeout: float
    resources: dict[str, Resource]
    booted: bool = False

    @staticmethod
    def current(request: fastapi.Request) -> 'ServiceClient':
        return request.app.client

    @staticmethod
    def boot(func: Callable[..., Any]) -> Callable[..., Any]:
        """Ensure that the client is booted and configured."""
        @functools.wraps(func)
        async def f(self: Any, *args: Any, **kwargs: Any) -> Any:
            if not self.booted:
                await self.on_boot()
                self.booted = True
            return await func(self, *args, **kwargs)
        return f

    def __init__(
        self,
        server: str,
        identity: ServiceIdentity,
        encrypter: PersonalDataHandler,
        logger: logging.Logger | None = None,
        timeout: float = 60.0
    ):
        self.credential = None
        self.encrypter = encrypter
        self.identity = identity
        self.logger = logger or logging.getLogger("uvicorn")
        self.resources = {}
        self.server = server
        self.timeout = timeout

    @boot
    async def configure(self, resource: str) -> Resource:
        """Configure the named resource `resource` and return a
        :class:`~cbra.ext.service.Resource` instance.
        """
        if resource not in RESOURCE_SERVERS:
            raise ValueError(f"Resource not configured: {resource}")
        if resource not in self.resources:
            url = RESOURCE_SERVERS[resource]['server']
            self.resources[resource] = Resource(
                server=url,
                credential=await self.get_credential(
                    scope=RESOURCE_SERVERS[resource].get('scope') or set(),
                    resource=url
                )
            )
            await self.resources[resource].connect()
            self.logger.info("Configured resource server %s", url)
        return self.resources[resource]

    @boot
    async def get_client_assertion(self, audience: str | None = None) -> str:
        """Encode a client assertion used to authenticate with the authorization
        server.
        """
        return await self.identity.get_client_assertion(
            token_endpoint=audience or self.metadata.token_endpoint
        )

    @boot
    async def get_credential(
        self,
        scope: set[str],
        resource: str | None = None
    ) -> Credential:
        """Obtain a credential for the given resource."""
        return await Credential.obtain(
            http=self.http,
            token_endpoint=self.metadata.token_endpoint,
            client_id=self.identity.client_id,
            assertion_factory=self.get_client_assertion,
            scope=scope,
            resource=resource
        )

    async def decrypt(self, *args: Any, **kwargs: Any) -> bytes | dict[str, Any] | str:
        """Encrypt data from storage purposes."""
        return await self.encrypter.decrypt(*args, **kwargs)

    async def encrypt(self, *args: Any, **kwargs: Any) -> str:
        """Encrypt data for storage purposes."""
        return await self.encrypter.encrypt(*args, **kwargs)

    @boot
    async def token(self, *, grant_type: str, **params: Any) -> TokenResponse:
        """Request a grant from the token endpoint of the configured
        authorization server using client credentials.
        """
        params.update({
            'grant_type': grant_type,
            'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
            'client_assertion': await self.get_client_assertion(),
            'client_id': self.identity.client_id
        })
        response = await self.http.post( # type: ignore
            url=self.metadata.token_endpoint,
            json=params
        )
        if response.status_code >= 400:
            if str.startswith(response.headers.get('Content-Type', ''), 'application/json'):
                dto = response.json()
                self.logger.critical(
                    "Unable to obtain token (error: %s, description: %s)",
                    dto.get('error', '')[:256],
                    dto.get('error_description', '')[:256]
                )
                raise UpstreamServiceNotAvailable
            else:
                response.raise_for_status()
        return TokenResponse.parse_obj(response.json())

    @retry(15, interval=1.0, exception=UpstreamFailure, only=Retryables)
    async def get_server_jwks(self) -> JSONWebKeySet | None:
        self.logger.info("Obtaining JWKS for server %s", self.server)
        return await self.metadata.get_jwks(self.http)

    @retry(15, interval=1.0, exception=UpstreamFailure)
    async def get_server_metadata(self) -> ServerMetadata:
        self.logger.info("Obtaining metadata for server %s", self.server)
        return await ServerMetadata.discover(self.http, self.server)

    async def on_boot(self):
        try:
            self.logger.info("Booting service client")
            self.http = await AsyncClient(timeout=self.timeout).__aenter__()
            self.metadata = await self.get_server_metadata()
            self.jwks = await self.get_server_jwks()
        except AuthorizationServerNotDiscoverable:
            self.logger.fatal("Unable to discover authorization server %s", self.server)
            raise
        self.logger.info("Succesfully discovered authorization server %s", self.server)
        if not self.metadata.token_endpoint:
            self.logger.critical(
                "The authorization server did not advertise a token endpoint."
            )
            raise AuthorizationServerMisbehaves

    @boot
    async def introspect(self, access_token: str) -> IntrospectionResponse:
        """Introspect the given access token using the Token Introspection
        Endpoint of the configured authorization server.
        """
        if not self.metadata.introspection_endpoint:
            raise NotImplementedError(
                "The authorization server does not support introspection."
            )
        if not self.credential:
            self.credential = await self.get_credential(
                scope={"oauth2.introspect"},
                resource=self.server
            )
        response = await self.http.post( # type: ignore
            url=self.metadata.introspection_endpoint,
            json={
                'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
                'client_assertion': await self.get_client_assertion(
                    audience=self.metadata.introspection_endpoint
                ),
                'client_id': self.identity.client_id,
                'token': access_token
            }
        )
        response.raise_for_status()
        return IntrospectionResponse.parse_obj(response.json())

    async def on_teardown(self):
        if self.booted:
            self.logger.info("Teardown service client")
            for resource in self.resources.values():
                await resource.close()
            await self.http.__aexit__(None, None, None)

    @boot
    @retry(15, interval=1.0, exception=UpstreamFailure, only=Retryables)
    async def request(
        self,
        method: str,
        resource: str,
        path: str,
        headers: dict[str, str] | None = None,
        **kwargs: Any
    ):
        """Make a HTTP request to the specified resource and path."""
        if resource not in self.resources:
            await self.configure(resource)
        svc = self.resources[resource]
        response = await svc.request(
            method=method,
            path=path,
            headers=headers,
            **kwargs
        )
        error_code: str | None = response.headers.get('X-Error-Code')
        if error_code == 'TOKEN_EXPIRED':
            assert svc.credential is not None # nosec
            await svc.credential.refresh()
            response = await svc.request(
                method=method,
                path=path,
                headers=headers,
                **kwargs
            )
        return response

    async def delete(
        self,
        resource: str,
        path: str,
        headers: dict[str, str] | None = None,
        **kwargs: Any
    ) -> Response:
        """Perform a DELETE request to the specified resource."""
        return await self.request(
            method="DELETE",
            resource=resource,
            path=path,
            headers=headers,
            **kwargs
        )

    async def get(
        self,
        resource: str,
        path: str,
        headers: dict[str, str] | None = None,
        **kwargs: Any
    ) -> Response:
        """Perform a POST request to the specified resource."""
        return await self.request(
            method="GET",
            resource=resource,
            path=path,
            headers=headers,
            **kwargs
        )

    async def post(
        self,
        resource: str,
        path: str,
        headers: dict[str, str] | None = None,
        **kwargs: Any
    ) -> Response:
        """Perform a POST request to the specified resource."""
        return await self.request(
            resource=resource,
            method="POST",
            path=path,
            headers=headers,
            **kwargs
        )