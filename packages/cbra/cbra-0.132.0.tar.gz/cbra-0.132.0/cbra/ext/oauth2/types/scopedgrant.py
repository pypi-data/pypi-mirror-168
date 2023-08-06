# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic

from .basegrant import BaseGrant
from .spaceseparatedlist import SpaceSeparatedList


class ScopedGrant(BaseGrant):
    scope: SpaceSeparatedList | set[str] | None = pydantic.Field(
        default=[],
        title="Scope",
        description=(
            "The requested scope that was previously granted to the subject "
            "or client."
        )
    )