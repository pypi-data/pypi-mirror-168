# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import inspect
from typing import Any

import pydantic


def is_openapi_schema(
    value: Any
) -> bool:
    """Return a boolean indicating if the object may be used as an OpenAPI
    schema.
    """
    return is_pydantic_model(value)


def is_pydantic_model(value: Any) -> bool:
    """Return a boolean indicating if the value is a :mod:`pydantic`
    model.
    """
    return inspect.isclass(value) and issubclass(value, pydantic.BaseModel)