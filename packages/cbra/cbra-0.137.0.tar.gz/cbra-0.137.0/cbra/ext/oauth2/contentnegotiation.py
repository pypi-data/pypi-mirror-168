"""Declares :class:`ContentNegotiation`."""
import ckms.jose
import fastapi

import cbra
from cbra.headers import ACCEPT
from cbra.headers import CONTENT_ENCODING
from cbra.headers import CONTENT_LENGTH
from cbra.headers import CONTENT_TYPE
from cbra.headers import WANTS_DIGEST
from cbra.negotiation import DefaultContentNegotiation
from .params import ClientRepository
from .params import LocalIssuer
from .params import ServerCodec
from .types import IClientRepository


class ContentNegotiation(DefaultContentNegotiation):
    __module__: str = 'cbra.ext.oauth2'
    clients: IClientRepository
    codec: ckms.jose.PayloadCodec
    issuer: str

    def __init__(
        self,
        request: fastapi.Request,
        accept: str = ACCEPT,
        content_encoding: str = CONTENT_ENCODING,
        content_length: int = CONTENT_LENGTH,
        content_type: str = CONTENT_TYPE,
        wants_digest: str | None = WANTS_DIGEST,
        clients: IClientRepository = ClientRepository,
        codec: ckms.jose.PayloadCodec = ServerCodec,
        issuer: str = LocalIssuer
    ):
        super().__init__(
            request=request,
            accept=accept,
            wants_digest=wants_digest
        )
        self.content_encoding = content_encoding
        self.content_length = content_length
        self.content_type = content_type
        self.clients = clients
        self.codec = codec
        self.issuer = issuer

    def select_parser(
        self, parsers: list[type[cbra.types.IParser]]
    ) -> cbra.types.IParser:
        parser = super().select_parser(parsers)
        parser.server_codec = self.codec # type: ignore
        parser.clients = self.clients # type: ignore
        parser.issuer = self.issuer # type: ignore
        return parser