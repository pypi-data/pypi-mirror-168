# type: ignore
"""Declares :class:`ClientConfig`."""
import secrets
import typing
from typing import Any, Literal

import httpx
import pydantic
from ckms.core.models import JSONWebSignature
from ckms.types import IKeychain
from ckms.types import JSONWebKey
from ckms.types import JSONWebKeySet
from ckms.types import JSONWebToken
from ckms.types import MalformedPayload
from ckms.jose import PayloadCodec

from cbra.utils import current_timestamp
from .baseclient import BaseClient
from .clientsubject import ClientSubject
from .exceptions import Error
from .exceptions import MissingRedirectURL
from .exceptions import RedirectForbidden
from .types import ISubject
from .types import GrantType
from .types import RedirectURL
from .types import ResponseType


class ClientConfig(BaseClient):
    InvalidCredential: type[Exception] = type('InvalidCredential', (Exception,), {})

    allow_key_discovery: bool = False

    allow_multiple_audiences: bool = False

    allowed_audience: typing.Set[str] = set()

    allowed_origins: typing.Set[str] = set()

    client_id: str

    client_secret: str | None = None

    default_redirect_url: RedirectURL | None = None

    first_party: bool = False

    grant_types_supported: list[GrantType] = []

    id_token_ttl: int = 3600

    jwks_uri: str | None = None

    keys: list[JSONWebKey] = []

    redirect_uris: list[RedirectURL] = []

    response_modes: set[str] = set()

    response_types: set[ResponseType] = set()

    scope: set[str] = set()

    subject_type: Literal["public", "pairwise"] = "pairwise"

    @property
    def jwks(self) -> JSONWebKeySet:
        return JSONWebKeySet(keys=self.keys)

    def __init__(self, **kwargs: typing.Any):
        redirect_uris = kwargs.setdefault('redirect_uris', [])
        if 'default_redirect_url' in kwargs:
            redirect_uris.append(kwargs['default_redirect_url'])
        super().__init__(**kwargs)

    def allows_audience(self, issuer: str, audience: typing.Set[str]) -> bool:
        """Return a boolean indicating if the client allows the issueing
        of access token for the given audiences set `audience`.
        """
        return (audience <= (self.allowed_audience | {issuer}))

    def allows_grant_type(self, grant_type: GrantType) -> bool:
        """Return a boolean indicating if the client allows the
        given grant type.
        """
        return grant_type.value in self.grant_types_supported

    def allows_origin(self, origin: str | None) -> bool:
        """Return a boolean indicating if the client allows the given origin in the
        context of Cross-Origin Resource Sharing (CORS).
        """
        return origin is None or origin in self.allowed_origins

    def allows_response_mode(self, response_mode: Any) -> bool:
        """Return a boolean indicating if the client allows the given response
        mode.
        """
        return response_mode in self.response_modes

    def allows_response_type(self, response_type: ResponseType) -> bool:
        """Return a boolean indicating if the client allows the given response
        type.
        """
        return response_type in self.response_types

    def allows_scope(self, scope: set[str]) -> bool:
        """Return a boolean indicating if the client allows the given scope."""
        return bool(set(scope) <= self.scope)

    def as_subject(self) -> ISubject:
        """Return a :class:`~cbra.ext.oauth2.types.ISubject` implementation
        representing the client itself. For use with the client credentials
        grant.
        """
        return ClientSubject(client_id=self.client_id)

    def can_issue_multiple(self) -> bool:
        """Return a boolean indicating if the client allows issueing
        access tokens to multiple audiences.
        """
        return self.allow_multiple_audiences

    def can_redirect(self, url: typing.Union[str, RedirectURL]) -> bool:
        """Return a boolean indicating if the client allows
        redirects to the given `url`.
        """
        return url in self.redirect_uris

    def get_default_redirect(self) -> str:
        """Return the default redirect URL, if specified."""
        return self.default_redirect_url

    def get_encryption_keys(self) -> list[JSONWebKey]:
        """Return the encryption keys used by the client."""
        return [x for x in self.keys if x.use == "enc"]

    def get_id_token_claims(self, now: int) -> dict[str, Any]:
        return {
            'aud': [self.client_id],
            'azp': self.client_id,
            'exp': now + self.id_token_ttl
        }

    def get_redirect_url(
        self,
        url: str | RedirectURL | None = None,
        fatal: bool = True
    ) -> RedirectURL | None:
        """Return a :class:`RedirectURL` instance that the server is
        allowed to redirect to.
        """
        # If there is no URL or a single redirect URL, then the
        # client is allowed to omit the redirect_uri parameter.
        if not url and len(self.redirect_uris) == 1:
            return self.redirect_uris[0]

        # If multiple redirect URIs have been registered, the client
        # MUST include a redirect URI with the authorization request
        # using the "redirect_uri" request parameter (OAuth 2.1 draft,
        # 2.3.3).
        try:
            if url is None and len(self.redirect_uris) > 1:
                raise MissingRedirectURL
            if url is None and self.redirect_uris:
                url = self.redirect_uris[0]
            if not self.redirect_uris:
                raise RedirectForbidden

            if not isinstance(url, RedirectURL):
                url = RedirectURL.validate(url)
            if not self.can_redirect(url):
                raise RedirectForbidden
        except Error:
            if fatal:
                raise
            url = None
        return url

    def get_subject_id(self, subject: ISubject) -> int:
        """Return the subject identifier to add to an access token or ID
        token.
        """
        return subject.get_identifier(public=self.subject_type == "public")

    async def import_jwks(self) -> JSONWebKeySet:
        """Retrieve the JSON Web Key Set (JWKS) that is specified by the
        :attr:`jwks_uri` attribute.
        """
        jwks = self.jwks or JSONWebKeySet()
        if jwks or not self.jwks_uri:
            return jwks
        async with httpx.AsyncClient() as client:
            response = await client.get(self.jwks_uri)
            if response.status_code == 200:
                try:
                    self.jwks = jwks = JSONWebKeySet.parse_obj(response.json())
                except pydantic.ValidationError as e:
                    pass
        return jwks

    def is_first_party(self) -> bool:
        """Return a boolean indicating if this is a first-party client
        that does not have to obtain consent.
        """
        return self.first_party

    async def issue_token(
        self,
        codec: PayloadCodec,
        using: str,
        issuer: str,
        audience: typing.Union[str, typing.Set[str]],
        subject: ISubject,
        ttl: int,
        scope: typing.Set[str]
    ) -> str:
        """Issue an access token encoded as a JSON Web Token (JWT)
        as defined in :rfc:`9068`. Return a string containing the
        token.
        """
        claims = {
            'aud': list(audience),
            'client_id': self.client_id,
            'iss': issuer,
            'jti': secrets.token_urlsafe(24),
            'scope': str.join(' ', sorted(scope)),
            'sub': self.get_subject_id(subject),
        }
        if scope:
            claims['scope'] = ' '.join(sorted(x for x in scope))

        # The scope claim can be removed if it is empty because "if an
        # authorization request includes a scope parameter, the
        # corresponding issued JWT access token SHOULD include a "scope"
        # claim as defined in Section 4.2 of [RFC8693]." (RFC 9068, 2.2.3)
        if not scope:
            claims.pop('scope')

        now = claims['iat'] = current_timestamp()
        claims.update({
            'exp': now + ttl,
            'nbf': now,
        })
        return await codec.encode(
            JSONWebToken(**claims),
            content_type="at+jwt",
            signers=[using]
        )

    def is_confidential(self) -> bool:
        """Return a boolean indicating if the client is confidential."""
        return bool(self.jwks_uri or self.keys or self.client_secret)

    def is_public(self) -> bool:
        """Return a boolean indicating if the client is public."""
        return self.client_secret is None and not self.keys

    async def verify_jws(
        self,
        jws: JSONWebSignature
    ) -> bool:
        """Verify a :class:`~ckms.jose.JSONWebSignature` using the public
        keys associated to the client.
        """
        jwks = self.jwks
        if self.jwks_uri:
            jwks = await self.import_jwks()
        return await jws.verify(jwks)

    async def verify_jwt(
        self,
        token: typing.Union[bytes, str],
        decrypter: typing.Optional[IKeychain],
        compact_only: bool = False,
        audience: str | None = None
    ) -> JSONWebToken:
        """Verifies a JSON Web Token (JWT) using the public keys of the
        client.

        Args:
            token (byte-sequence or string): the JWT to deserialize and
                verify.
            decrypter: a :class:`~IKeychain` implementation that has the
                private keys to decrypt, if the payload is a JWE.
            compact_only (bool): indicates if only compact deserialization
                is allowed. If `compact_only` is ``True`` and the token
                is not compact serialized, an exception is raised.

        Returns
            A :class:`dict` containing the claims in the JWT.
        """
        codec = PayloadCodec(decrypter=decrypter, verifier=self.jwks)
        if isinstance(token, str): # pragma: no cover
            token = str.encode(token, 'ascii')
        jwt = await codec.decode(token, accept="jwt")
        if not isinstance(jwt, JSONWebToken):
            raise MalformedPayload(message="A JSON Web Token (JWT) is expected.")
        jwt.verify(audience={audience} if audience else set())
        return jwt