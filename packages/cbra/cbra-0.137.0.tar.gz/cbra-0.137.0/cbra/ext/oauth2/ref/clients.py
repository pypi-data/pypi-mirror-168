# pylint: skip-file
from cbra.ext.oauth2 import ClientConfig
from cbra.ext.oauth2.types import GrantType
from cbra.ext.oauth2.types import ResponseMode


jwt: ClientConfig = ClientConfig(
    client_id='jwt',
    grant_types_supported=[
        GrantType.jwt_bearer.value
    ],
    response_modes=[
        ResponseMode.query
    ]
)