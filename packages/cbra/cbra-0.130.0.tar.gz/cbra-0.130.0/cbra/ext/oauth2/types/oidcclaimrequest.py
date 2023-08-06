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

from .invalidrequest import InvalidRequest


class OIDCClaimRequest(pydantic.BaseModel):
    essential: bool = False
    value: Any = None
    values: list[str | int] = pydantic.Field(
        default=[],
        max_items=10
    )

    @pydantic.root_validator(pre=True)
    def preprocess(
        cls,
        values: dict[str, Any]
    ) -> dict[str, Any]:
        if values.get('value') and values.get('values'):
            raise InvalidRequest(
                description=(
                    "The 'value' and 'values' parameters can not both be "
                    "specified."
                )
            )
        if values.get('value'):
            values['values'] = [ values.pop('value') ]
        return values

    @pydantic.validator('values')
    def validate_values(
        cls,
        values: list[Any]
    ) -> list[Any]:
        """Validates that the members of the input do not have excessive
        size.
        """
        for value in values:
            if isinstance(value, int):
                continue
            if isinstance(value, str) and len(value) > 512:
                raise ValueError("Requested claim value exceeds 512 characters.")
        return values

    def accepts(self, value: str) -> bool:
        """Return a boolean indicating if the :class:`OIDCClaimRequest`
        accepts the given value.
        """
        return not self.values or (value in self.values)