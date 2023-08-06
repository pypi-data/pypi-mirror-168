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
from typing import Callable
from typing import Coroutine

import fastapi
import fastapi.routing
from fastapi.dependencies.utils import get_body_field
from fastapi.dependencies.utils import get_dependant

from .types import Request


RESPONSE_MODEL_PARAMS: set[str] = {
    'response_model',
    'response_model_include',
    'response_model_exclude',
    'response_model_by_alias',
    'response_model_exclude_unset',
    'response_model_exclude_defaults',
    'response_model_exclude_none',
}


class APIRoute(fastapi.routing.APIRoute):
    """A custom :class:`fastapi.routing.APIRoute` implementation
    that accomodates the rendering of request examples for multiple
    content types.
    """

    def __init__(self, *args: Any, **kwargs: Any):
        # TODO: This here is a hack to remove unwanted stuff from the APIRoute
        # parameters.
        if kwargs.get('status_code') in (204, "204"):
            for param in RESPONSE_MODEL_PARAMS:
                kwargs.pop(param, None)
        super().__init__(*args, **kwargs)

        # Inspect the APIRoute.endpoint attribute to determine if we
        # need to do some magic the get a proper body model. Since
        # a number of handler functions does not declare the body
        # model using annotation, in order to be able to do explicit
        # parsing of the request body, it is not seen by FastAPI when
        # creating a route and rendering the OpenAPI schema. Thus, here
        # we look for some special types from which we can retrieve the
        # body model. This ensures that all models used by Endpoint
        # implementations are added to the schema.
        Model = getattr(self.endpoint, 'model', None)
        if Model is not None:
            # Create a fake dependant to trick get_body_field() into
            # getting the model.
            async def f(dto: Model) -> Any: pass # type: ignore
            self.body_field = get_body_field(
                dependant=get_dependant(path=self.path_format, call=f),
                name=self.unique_id
            )

    def get_route_handler(
        self
    ) -> Callable[[fastapi.Request], Coroutine[Any, Any, fastapi.Response]]:
        super_handler = super().get_route_handler()

        async def handler(request: fastapi.Request) -> fastapi.Response:
            return await super_handler(
                Request(request.scope, request.receive)
            )

        return handler