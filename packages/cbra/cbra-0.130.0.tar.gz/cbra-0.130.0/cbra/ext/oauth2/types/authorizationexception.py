# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import logging
from typing import NoReturn

from cbra.exceptions import HTTPException
from .promptexception import PromptException
from .redirecturl import RedirectURL


class AuthorizationException(HTTPException):
    """Base class for errors during an Authorization Request, not including
    configuration or request parameter errors."""
    __module__: str = 'cbra.ext.oauth2.types'
    log_level: str = 'INFO'

    def log(self, logger: logging.Logger) -> None:
        """Create a log record of this error."""
        raise NotImplementedError

    def raise_for_user(self, url: str, redirect_uri: RedirectURL) -> NoReturn:
        """Raises the exception with an indication that it must be
        displayed to the end-user, within the trust boundaries of
        the authorization server.
        """
        raise PromptException(url, {
            'return_uri': redirect_uri.error(error='access_denied')
        })