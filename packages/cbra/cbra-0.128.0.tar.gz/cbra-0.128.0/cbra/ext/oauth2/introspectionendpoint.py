# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from ckms.jose import PayloadCodec

from cbra.endpoint import Endpoint
from cbra.exceptions import Forbidden
from .currentclient import CurrentClient
from .params import ServerCodec
from .params import SubjectRepository
from .types import IClient
from .types import ISubjectRepository
from .types import IntrospectionRequest
from .types import IntrospectionResponse


class IntrospectionEndpoint(Endpoint):
    __module__: str = 'cbra.ext.oauth2'
    methods: list[str] = ["POST"]
    summary: str = "Introspection Endpoint"
    model: type[IntrospectionRequest] = IntrospectionRequest
    subjects: ISubjectRepository = SubjectRepository

    async def authorize(
        self,
        client: IClient = CurrentClient
    ) -> None:
        if not client.allows_scope({"oauth2.introspect"}):
            raise Forbidden

    async def handle( # type: ignore
        self,
        dto: IntrospectionRequest,
        codec: PayloadCodec = ServerCodec,
        client: IClient = CurrentClient,
    ) -> IntrospectionResponse:
        jws, jwt = await codec.jwt(dto.token, accept="at+jwt")
        subject = await self.subjects.get(
            client=client,
            subject_id=jwt.sub
        )
        if subject is None:
            return IntrospectionResponse(active=False)

        params: dict[str, Any] = {
            **jwt.dict(),
            'active': await jws.verify(codec.verifier)
        }
        if subject is not None:
            params.update({
                'sub': subject.sub
            })
        return IntrospectionResponse.parse_obj(params)