# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi
from ckms.jose import PayloadCodec

from cbra.exceptions import Forbidden
from .params import ClientRepository
from .params import ServerCodec
from .types import ClientAssertion
from .types import IClient
from .types import IClientRepository


__all__: list[str] = ['CurrentClient']


async def get_current_client(
    request: fastapi.Request,
    assertion: ClientAssertion,
    clients: IClientRepository = ClientRepository,
    codec: PayloadCodec = ServerCodec
) -> IClient:
    if assertion.client_assertion is None:
        raise Forbidden
    jws, jwt = await codec.jwt(assertion.client_assertion)
    if jwt.iss is None:
        raise Forbidden
    client = await clients.get(jwt.iss)
    if client is None:
        raise Forbidden

    # Verify that the JWT has the proper audience and was signed by
    # this client.
    jwt.verify(audience={str(request.url)})
    if not await client.verify_jws(jws):
        raise Forbidden(
            message="The signature is not valid for the asserted client."
        )
    return client


CurrentClient: IClient = fastapi.Depends(get_current_client)