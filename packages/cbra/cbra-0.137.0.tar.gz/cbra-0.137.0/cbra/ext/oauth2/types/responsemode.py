# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""Declares :class:`ResponseMode`."""
import enum


class ResponseMode(str, enum.Enum):
    __module__: str = 'cbra.ext.oauth2.types'
    jwt = "jwt"
    fragment = "fragment"
    query = "query"