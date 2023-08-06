# type: ignore
"""Declares common exceptions classes."""
import copy
import typing
import fastapi
import urllib.parse
from typing import Any

import pydantic
import fastapi.responses
from fastapi.exceptions import RequestValidationError
from unimatrix.exceptions import CanonicalException
from unimatrix.exceptions import CanonicalExceptionMetaclass

from cbra.headers import CORS_HEADERS
from cbra.headers import DIGEST_SCHEMA
from cbra.types import ICanonicalException
from cbra.types import IContentNegotiation
from cbra.types import IParser
from cbra.types import IRenderer
from cbra.types import IRequestHandler
from cbra.utils import DeferredException



class HTTPException(Exception):
    """Mixin class for exceptions that can be converted to a response."""
    __module__: str = 'cbra.exceptions'

    async def as_response(self) -> fastapi.responses.Response:
        raise NotImplementedError


class IExceptionSpec(pydantic.BaseModel):
    code: str = pydantic.Field(
        default=...,
        title="Code",
        description=(
            "Further specifies the error condition in addition to the "
            "`kind` parameter."
        )
    )

    message: str = pydantic.Field(
        default=...,
        title="Message",
        description=(
            "A message describing the error. Note that this message "
            "is not intended for display to the end-user."
        )
    )

    hint: str | None = pydantic.Field(
        default=None,
        title="Hint",
        description=(
            "A hint describing possible actions to perform in order "
            "to resolve the error condition."
        )
    )


class BaseExceptionSpec(IExceptionSpec):
    detail: str

    @classmethod
    def for_code(
        cls,
        name: str,
        codes: list[str]
    ) -> typing.Any:
        return type(f'{name}Spec', (cls,), {
            'code': pydantic.Field(
                default=...,
                title="Error code",
                description=(
                    "A code describing the error that occurred. Clients "
                    "should use this code to determine the error condition."
                ),
                enum=codes
            ),
            '__annotations__': {
                'code': str
            },
            'Config': type('Config', (object,), {
                'title': f'{name}Spec'
            })
        })

    class Config:
        title = "ExceptionSpec"


class BaseRedirectingException(Exception):
    redirect_to: str
    params: dict[str, typing.Any] | None = None
    status_code: int = 303

    def __init__(
        self,
        redirect_to: str,
        params: dict[str, typing.Any] | None = None
    ) -> None:
        self.redirect_to = redirect_to
        self.params = params or {}

    def as_response(self) -> fastapi.responses.Response:
        return fastapi.responses.RedirectResponse(
            url=self.get_redirect_url(),
            status_code=self.status_code
        )

    def get_redirect_url(self) -> str:
        url = self.redirect_to
        if self.params:
            url = f'{url}?{urllib.parse.urlencode(self.params)}'
        return url

    def __repr__(self) -> str:
        return f"<LoginRequired: {self.get_redirect_url()}>"


class ValidationErrorSpec(BaseExceptionSpec):
    fieldErrors: typing.Dict[str, typing.List[typing.Any]] = {}

    class Config: # type: ignore
        title = "ValidationErrorSpec"


class ExceptionMetadata(pydantic.BaseModel):
    id: str = pydantic.Field(...,
        title="Identifier",
        description=(
            "Identifies the error. May be used to trace an error "
            "instance in logs."
        ),
        example="681b9604-df4e-4b2c-998c-9807a5569b1c"
    )

    timestamp: int = pydantic.Field(...,
        title="Timestamp",
        description=(
            "The date/time at which the error occurred, in milliseconds "
            "since the UNIX epoch."
        ),
        example=1647626707914
    )


class ExceptionModel(pydantic.BaseModel):
    apiVersion: typing.Literal['v1'] = pydantic.Field(...,
        title="API version",
        description="Schema version",
        example="v1"
    )
    metadata: ExceptionMetadata
    spec: BaseExceptionSpec

    @classmethod
    def parse_exc(
        cls,
        exception_class: type['CanonicalException'],
        data: dict[str, Any]
    ) -> 'CanonicalException':
        """Parse the exception data and return an instance of the given class."""
        obj = cls.parse_obj(data)
        return exception_class(id=obj.metadata.id, **obj.spec.dict())


class CanonicalExceptionMetaclass(CanonicalExceptionMetaclass):

    def __new__(cls: type, name: str, bases: list[str], attrs: dict[str, Any]):
        """Create a new :class:`CanonicalException` class."""
        new = super().__new__
        if attrs.pop('__abstract__', False):
            if name == 'CanonicalException':
                attrs['codes'] = {}
            return new(cls, name, bases, attrs)

        # Get the version and spec attributes to construct a pydantic model
        # description the exception.
        version: int = attrs.pop('version', 'v1')
        spec: type[BaseExceptionSpec] = attrs.pop('spec', BaseExceptionSpec)
        attrs['model'] = type(name, (ExceptionModel,), {
            '__annotations__': {'spec': spec},
            'spec': pydantic.Field(
                default=...,
                title=f'{name}Spec',
                description="Error condition parameters."
            )
        })
        return new(cls, name, bases, attrs)


class CanonicalException(CanonicalException, metaclass=CanonicalExceptionMetaclass):
    __abstract__: bool = True
    codes: dict[str, Any]
    model: type[ExceptionModel]
    include_in_schema: bool = True
    spec: type[IExceptionSpec] = BaseExceptionSpec

    @classmethod
    def defer(cls, **kwargs: typing.Any) -> DeferredException:
        return DeferredException(cls(**kwargs))

    @staticmethod
    def parse(code: str, data: dict[str, Any]) -> 'CanonicalException':
        for cls in CanonicalException.registered:
            if cls.code == code:
                break
        else:
            cls = None
        if cls is None or not hasattr(cls, 'spec'):
            return None
        return cls.model.parse_exc(cls, data)

    async def handle(
        self,
        request: fastapi.Request,
        handler: IRequestHandler,
        renderer: IRenderer
    ) -> fastapi.Response:
        """Renders the exception to a :class:`fastapi.responses.Response`
        instance.
        """
        if not renderer.has_content():
            return fastapi.Response(
                headers=self.get_http_headers(),
                status_code=self.http_status_code
            )

        return fastapi.Response(
            content=renderer.render(self.as_dict()),
            headers=self.get_http_headers(),
            status_code=self.http_status_code,
            media_type=renderer.get_response_encoding()
        )


class MissingScope(CanonicalException):
    __module__: str = 'cbra.exceptions'
    missing: set[str]
    http_status_code: int = 401
    code: str = "INVALID_SCOPE"
    message: str = "The access credential did not have the required scope."
    hint: str = (
        "Request the scope described by the 'missing' parameter from the "
        "authorization server."
    )

    class spec(IExceptionSpec):
        missing: list[str] = pydantic.Field(
            default=...,
            title="Required scope",
            description=(
                "The list of scopes that the principal needs to obtain "
                "to allow the request."
            )
        )

    def __init__(self, missing: set[str], **kwargs: Any):
        self.missing = missing
        super().__init__(**kwargs)

    def as_dict(self) -> dict[str, Any]:
        dto = super().as_dict()
        dto['spec']['missing'] = list(self.missing)
        return dto

    def upgrade_scope(self, scope: set[str]) -> set[str]:
        """Return a set holding the input scope and the required
        scope.
        """
        return set(self.missing) | scope


class UncaughtException(CanonicalException):
    http_status_code: int = 500


class Forbidden(CanonicalException):
    """Raised when the request is unconditionally rejected."""
    code = "FORBIDDEN"
    http_status_code = 403
    message = "The request was unconditionally rejected. That's all we know."


class WebhookMessageRejected(CanonicalException):
    """Raised when an incoming webhook message is rejected."""
    code: str = 'WEBHOOK_EVENT_REJECTED'
    http_status_code: int = 403
    message: str = "The server rejected the message."


class AuthenticationRequired(CanonicalException):
    """Raised when an operation required authenticated requests."""
    code = 'AUTHENTICATION_REQUIRED'
    http_status_code = 401
    message = "The operation requires authenticated requests."
    detail = (
        "An operation against a protected resource was attempted and it does "
        "not allow interactions with unauthenticated requests."
    )


class InvalidAuthorizationScheme(AuthenticationRequired):
    """Raised when the ``Authorization`` header had an invalid scheme."""
    code = 'INVALID_AUTHORIZATION_SCHEME'
    http_status_code = 403
    message = "The scheme provided in the Authorization header is not supported."
    detail = (
        "The server could not parse the credential in the Authorization header "
        "because the specified scheme is unknown or not allowed."
    )


class UntrustedIssuer(AuthenticationRequired):
    """Raised when a token was presented but the issuer is not trusted."""
    code: str = "UNTRUSTED_ISSUER"
    http_status_code: int = 403
    message: str = "The security token was issued by an untrusted party."

    def __init__(self, issuer: str):
        super().__init__(
            detail=(
                "The server has not established a trust relationship with "
                "the issuer ({issuer}) that supplied the security token. "
                "Consult the server documentation on the list of trusted "
                "issuers."
            )
        )


class MisbehavingIssuer(AuthenticationRequired):
    """Raised when an issuer is trusted, but there were problems retrieving
    its metadata or JSON Web Key Set (JWKS).
    """
    __module__: str = 'ckms.exceptions'
    code: str = 'MISBEHAVING_ISSUER'
    http_status_code: int = 403
    message: str = "The issuer is trusted but protocol errors occurred."


class UnreachableIssuer(AuthenticationRequired):
    """Raised when the issuer is trusted but no metadata could be discovered."""
    __module__: str = 'ckms.exceptions'
    code: str = 'UNREACHABLE_ISSUER'
    http_status_code: int = 403
    message: str = "The issuer is trusted but it was not reachable."


class ForgedAccessToken(AuthenticationRequired):
    """Raised when the parameters of a token were valid but it was not
    issued by a trusted entity.
    """
    code: str = "FORGED_ACCESS_TOKEN"
    http_status_code: int = 403
    message: str = "The security token was valid but not signed by a trusted party."
    detail: str = (
        "The claims presented with the security token validated against the server "
        "policy, but the digital signature did not validate against any of the known "
        "(public) keys. This incident is being logged, including your IP address "
        "and/or a browser fingerprint, and may lead to further escalation, "
        "such as criminal proscecution."
    )
    hint: str = "Stop forging security tokens."


class NotAuthorized(CanonicalException):
    """Raised when a request is not authorized to perform a given operation."""
    code = 'UNAUTHORIZED'
    http_status_code = 403
    message = "This request attempts an unauthorized action."
    detail = (
        "The credentials provided with the request did not resolve to a "
        "principal that was authorized to perform the action."
    )


class BearerAuthenticationRequired(AuthenticationRequired):
    hint = "Provide valid credentials using the Authorization header."


class NotFound(CanonicalException):
    code: str = 'NOT_FOUND'
    http_status_code: int = 404
    message: str = "No resource exists at the given URL."
    detail: str = (
        "The URL requested did not resolve to an existing resource."
    )


class InvalidPathParameter(NotFound):
    code: str = 'INVALID_PATH_PARAMETER'
    message: str = "The path parameter(s) did identify an existing resource."


class NotAcceptable(CanonicalException):
    """Generic exception that is raised when any of the ``Accept``,
    ``Accept-Encoding`` or ``Accept-Language`` headers can not be
    satisfied by the server.
    """
    __module__: str = 'cbra.exceptions'
    http_status_code: int = 406
    code: str = 'NOT_ACCEPTABLE'
    message: str = "The request's content negotiation is unacceptable."
    detail: str = (
        "The server cannot produce a response matching the list of "
        "acceptable values defined in the request's proactive content "
        "negotiation headers, and is unwilling to supply a default "
        "representation."
    )


class MediaTypeNotAcceptable(NotAcceptable):
    """Raised when the media type specified in the ``Accept`` header is
    not acceptable.
    """
    code: str = 'MEDIA_TYPE_NOT_ACCEPTABLE'


class UpstreamServiceNotAvailable(CanonicalException):
    """Raised when the application is not able to establish
    a (network) connection to an upstream service.
    """
    code = 'SERVICE_NOT_AVAILABLE'
    http_status_code = 503
    message = "The service is currently not available."
    detail = (
        "Network or other infrastructure issues prevent "
        "proper operation of the service."
    )
    hint = "Try again later."
    retry_after: int | None = None

    def __init__(self, retry_after: int | None = None, **kwargs: Any):
        self.retry_after = retry_after
        if retry_after is not None:
            kwargs['hint'] = f'Try again in {retry_after} seconds.'
        super().__init__(**kwargs)

    def get_http_headers(self) -> dict[str, str]:
        return  {
            **super().get_http_headers(),
            'Retry-After': str(self.retry_after or 120)
        }


class UpstreamConnectionFailure(UpstreamServiceNotAvailable):
    """Raised when an upstream service listens at the configured address
    and port, but there are issued in establish the connection according
    to the agreed protocol. Such errors may occur when, for example, the
    upstream service is booting and has bound to its address and port, but
    is not yet ready to serve.
    """
    hint = "Try again in 10 seconds."


class TrustIssues(CanonicalException):
    http_status_code = 403
    code = "TRUST_ISSUES"
    message = (
        "The credential attached to the request was issued by an unkown "
        "authority."
    )
    hint = (
        "Verify that the credential (i.e. bearer token or X.509 certificate) "
        "was issued by an authority that is trusted by this system."
    )


class TryAgain(CanonicalException):
    code = 'SERVICE_NOT_AVAILABLE'
    http_status_code = 503
    message = "The service is currently not available."
    detail = (
        "Network or other infrastructure issues prevent "
        "proper operation of the service."
    )
    hint = "Try again in 600 seconds."

    def __init__(self, retry_after): # pragma: no cover
        super().__init__()


class UnsupportedMediaType(CanonicalException):
    http_status_code = 415
    code = "UNSUPPORTED_MEDIA_TYPE"
    message = "The server does not understand the request media type."

    @classmethod
    def fromparsers(cls, parsers: typing.List[typing.Type[IParser]]):
        return cls([x.media_type for x in parsers])

    def __init__(self, accepts: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.accepts = accepts

    def get_http_headers(self) -> dict:
        return {
            **super().get_http_headers(),
            'Accept': str.join(', ', self.accepts)
        }


class MissingContentTypeHeader(UnsupportedMediaType):
    __module__: str = 'cbra.exceptions'
    code: str = 'MISSING_CONTENT_TYPE_HEADER'
    message: str = (
        "The server does not understand the request media type because it "
        "did not provide the Content-Type header."
    )


class ParseError(CanonicalException):
    http_status_code = 400
    code = "MALFORMED_BODY"
    message = (
        "The server understands the media type but the request body "
        "is malformed."
    )


class InvalidHeaderValue(CanonicalException):
    http_status_code: int = 400
    code: str = "INVALID_HEADER_VALUE"

    def __init__(self, name: str, value: typing.Any = None, **kwargs: typing.Any):
        super().__init__(
            message=(
                f"The {name} header contained an illegal value."
                if value is not None else
                f"The {name} header contained an illegal value: '{value}'."
            )
        )


class UnsupportedDigestAlgorithm(CanonicalException):
    http_status_code: int = 400
    code: str = 'UNSUPPORTED_RESPONSE_DIGEST'
    message: str = (
        "None of the requested response digest algorithms is supported "
        "by the server."
    )
    hint: str = "Inspect the Wants-Digest header for the available algorithms."

    def __init__(self, supported: typing.Set[str]):
        super().__init__(
            detail=f"Supported algorithms are: {', '.join(supported)}."
        )
        self.supported = supported

    async def handle(
        self,
        request: fastapi.Request,
        handler: IRequestHandler,
        renderer: IRenderer
    ) -> fastapi.Response:
        response = await super().handle(request, handler, renderer)
        response.headers['Wants-Digest'] = ', '.join(self.supported)
        return response


class MissingRequestBody(CanonicalException):
    http_status_code: int = 422
    code: str = 'BODY_REQUIRED'
    message: str = "This endpoint requires a request body."
    detail: typing.Optional[str] = None
    hint: typing.Optional[str] = None


class UnprocessableEntity(CanonicalException):
    """Test"""
    http_status_code: int = 422
    code: str = "UNPROCESSABLE_ENTITY"
    message: str = "The server was not able to process the request."
    detail: str = (
        "The server understands the content type of the request entity, and "
        "the syntax of the request entity is correct, but it was unable to "
        "process the contained instructions."
    )
    hint: str = "Inspect the .spec.fieldErrors member for additional details."

    @classmethod
    def fromexc(
        cls,
        exception: typing.Union[pydantic.ValidationError, RequestValidationError]
    ):
        errors = {}
        for error in exception.errors():
            location = error['loc']
            if error['loc'][0] == 'body' and len(error['loc']) == 1:
                instance = MissingRequestBody()
                break
            elif location[0] == 'path':
                # A validation error in the path parameter suggests that
                # such a resource does not exist, assuming that the path
                # parameter is properly types.
                return InvalidPathParameter()
            elif exception.model:
                instance = cls()
            else:
                location, field = error['loc']
                if location not in errors:
                    errors[location] = []
        else:
            instance = cls(errors=errors)
        return instance


class Unserializable(ValueError):
    pass


def get_exception_headers(
    status_code: int
) -> typing.Dict[str, typing.Any]:
    return {
        **CORS_HEADERS,
        'Digest': DIGEST_SCHEMA,
        'X-Error-Code': {
            'description': "The error code describing the exception that occurred.",
            'schema': {
                'type': "string",
                'enum': sorted(set([
                    cls.code
                    for cls in CanonicalException.registered
                    if cls.http_status_code == status_code
                ]))
            }
        },
    }


def get_exception_models(
    status_code: int,
    name: str
) -> typing.TypeVar:
    codes = list(sorted(set([
        cls.code
        for cls in CanonicalException.registered
        if cls.http_status_code == status_code
    ])))
    return type(name, (ExceptionModel,), {
        'kind': pydantic.Field(
            default=...,
            title="Kind",
            description=f"Is always `{name}`."
        ),
        'spec': pydantic.Field(
            default=...,
            title="Specification",
            description="A datastructure describing the error."
        ),
        '__annotations__': {
            'kind': typing.Literal[name],
            'spec': BaseExceptionSpec.for_code(name, codes)
        }
    })


EXCEPTION_RESPONSES: dict[int | str, typing.Any] = {
    400: {
        'headers': get_exception_headers(400),
        'description': "The request is malformed.",
        'model': get_exception_models(400, 'BadRequest'),
    },
    401: {
        'headers': get_exception_headers(401),
        'description': (
            "Authentication or privilege escalation is required for this endpoint."
        ),
        'model': get_exception_models(401, 'NotAuthorized')
    },
    403: {
        'headers': get_exception_headers(403),
        'description': "The request was unconditionally rejected.",
        'model': get_exception_models(403, 'Forbidden')
    },
    406: {
        'headers': get_exception_headers(406),
        'description': (
            "The requested content representation is not supported by the server."
        ),
        'model': get_exception_models(406, 'NotAcceptable')
    },
    415: {
        'headers': get_exception_headers(415),
        'description': "The server does not understand the request media type.",
        'model': get_exception_models(415, 'UnsupportedMediaType')
    },
    422: {
        'headers': get_exception_headers(422),
        'description': "The content of the request was semantically invalid.",
        'model': get_exception_models(422, 'UnprocessableEntity')
    },
    500: {
        'headers': get_exception_headers(500),
        "description": (
            "An unrecoverable exception occurred while processing the request."
        ),
        'model': get_exception_models(500, 'InternalServerError')
    },
    503: {
        'headers': get_exception_headers(503),
        'description': (
            "The service or an upstream service is not available."
        ),
        'model': get_exception_models(503, 'ServiceNotAvailable')
    }
}


def get_exception_response(
    code: int | str,
    headers: dict[str, typing.Any],
    has_body: bool
) -> dict[str, typing.Any]:
    schema = copy.deepcopy(EXCEPTION_RESPONSES[code])
    if not has_body:
        schema.pop('model')
    return {
        **schema,
        'headers': headers
    }
