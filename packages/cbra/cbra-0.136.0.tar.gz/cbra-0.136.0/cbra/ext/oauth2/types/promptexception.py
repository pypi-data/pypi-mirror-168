# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import urllib.parse

import fastapi.responses

from cbra.exceptions import HTTPException


class PromptException(HTTPException):
    __module__: str = 'cbra.ext.oauth2.types'
    prompt_url: str
    parts: urllib.parse.ParseResult
    params: dict[str, str]

    def __init__(self, prompt_url: str, params: dict[str, str] | None = None) -> None:
        self.prompt_url = prompt_url
        self.parts = urllib.parse.urlparse(prompt_url)
        self.params = params or {}

    def get_redirect_uri(self) -> str:
        parts = list(self.parts)
        parts[4] = urllib.parse.urlencode(self.params, doseq=True)
        return urllib.parse.urlunparse(parts)

    async def as_response(self) -> fastapi.responses.Response:
        return fastapi.responses.RedirectResponse(
            url=self.get_redirect_uri(),
            status_code=303
        )