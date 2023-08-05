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


class IntrospectionResponse(pydantic.BaseModel):
    active: bool = pydantic.Field(
        default=...,
        title="Active",
        description="Token active status"
    )

    sub: Any = pydantic.Field(
        default=None,
        title="Subject",
        description="The public identifier of the Subject."
    )