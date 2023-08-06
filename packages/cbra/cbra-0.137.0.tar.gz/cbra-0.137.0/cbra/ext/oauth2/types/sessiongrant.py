# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""Declares :class:`SessionGrant`"""
import typing

import pydantic

from .granttype import GrantType
from .scopedgrant import ScopedGrant


class SessionGrant(ScopedGrant):
    __module__: str = 'cbra.ext.oauth2.types'

    grant_type: typing.Literal[GrantType.session] = pydantic.Field(
        default=...,
        title="Grant type",
        description=(
            "Must be `session`."
        ),
        example="session"
    )

    session: str = pydantic.Field(
        default=...,
        title="Session",
        description=(
            "A JWT representing an authenticated session, signed by a "
            "key that is trusted by the authorization server, and "
            "optionally encrypted."
        )
    )