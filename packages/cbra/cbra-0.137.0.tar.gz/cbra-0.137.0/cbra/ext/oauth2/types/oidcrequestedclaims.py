# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import pydantic

from .oidcclaimrequest import OIDCClaimRequest


Empty = type('Empty', (object,), {})

#: OpenID Connect Core default ID Token claims.
DEFAULT_CLAIMS: set[str] = {
    "iss",
    "sub",
    "aud",
    "exp",
    "iat",
    "auth_time",
    "nonce",
    "acr",
    "amr",
    "azp"
}

class OIDCRequestedClaims(pydantic.BaseModel):
    iss: OIDCClaimRequest | None = None
    sub: OIDCClaimRequest | None = None
    aud: OIDCClaimRequest | None = None
    exp: OIDCClaimRequest | None = None
    iat: OIDCClaimRequest | None = None
    auth_time: OIDCClaimRequest | None = None
    nonce: OIDCClaimRequest | None = None
    acr: OIDCClaimRequest | None = None
    amr: OIDCClaimRequest | None = None
    azp: OIDCClaimRequest | None = None
    gender: OIDCClaimRequest | None = None

    def accepts(self, claim: str, value: Any) -> bool:
        """Return a boolean indicating if the given `value` is acceptable
        to the given `claim`.
        """
        if not self.requests(claim):
            return False
        return getattr(self, claim).accepts(value)

    def get_allowed_values(self, claim: str) -> list[Any]:
        """Return the list of allowed values for the given claim."""
        if not self.requests(claim):
            return []
        return getattr(self, claim).values

    def get_scope(self) -> set[str]:
        """Return a set of strings representing the requested scope by
        these claims.
        """
        scope: set[str] = {"openid"}
        for field in self.__fields__:
            assert isinstance(field, str) # nosec
            if self.requests(field):
                scope.add(field)
        return scope

    def requests(self, claim: str) -> bool:
        """Return a boolean indicating if the given claim is requested."""
        if claim not in self.__fields__:
            return False
        if claim in DEFAULT_CLAIMS:
            return True
        return getattr(self, claim, None) is not None