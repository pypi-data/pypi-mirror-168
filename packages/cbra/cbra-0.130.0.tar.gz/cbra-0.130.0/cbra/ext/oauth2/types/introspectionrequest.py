# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic

from .clientassertiontype import ClientAssertionType


class IntrospectionRequest(pydantic.BaseModel):
    client_assertion_type: ClientAssertionType | None = pydantic.Field(
        default=None,
        title="Client assertion type",
        description=(
            "The authorization server supports the following client assertions "
            "to establish the identity of confidential OAuth 2.0 clients:\n\n"
            "`urn:ietf:params:oauth:client-assertion-type:jwt-bearer`\n\n"
            "Clients that have registered a public key sign a JWT using that "
            "key. The Client authenticates in accordance with **JSON Web Token "
            "(JWT) Profile for OAuth 2.0 Client Authentication and Authorization "
            "Grants** and **Assertion Framework for OAuth 2.0 Client Authentication "
            "and Authorization Grants**. The JWT must contain the following "
            "required Claim Values and may contain the following optional Claim "
            "Values:\n\n"
            "- `iss` - (Required) Issuer. This MUST contain the ``client_id`` of "
            "the OAuth Client.\n"
            "- `sub` - (Required) Issuer. This MUST contain the ``client_id`` of "
            "the OAuth Client.\n"
            "- `aud` - (Required) Value that identifies the authorization server "
            "as an intended audience. The authorization server must verify that "
            "it is an intended audience for the token. The Audience must be the "
            "URL of the authorization server's **Token Endpoint**.\n"
            "- `jti` - (Required) A unique identifier for the token, which can "
            "be used to prevent reuse of the token. These tokens must only be "
            "used once.\n"
            "- `exp` - (Required) Expiration time on or after which the ID "
            "Token must not be accepted for processing.\n"
            "- `iat` - (Optional) Time at which the JWT was issued."
        )
    )

    client_assertion: str | None = pydantic.Field(
        default=None,
        title="Client assertion",
        description=(
            "The client assertion used to authenticate a confidential OAuth 2.0 "
            "client. See `client_assertion_type` for the supported protocols and "
            "formats."
        )
    )

    token: str = pydantic.Field(
        default=...,
        title="Token",
        description=(
            "The token to introspect. Must be issued by this authozation "
            "server."
        )
    )