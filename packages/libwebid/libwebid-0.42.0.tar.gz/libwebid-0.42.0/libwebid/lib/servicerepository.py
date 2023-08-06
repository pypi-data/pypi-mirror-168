# Copyright (C) 2022 Cochise Ruhulessin
# 
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import logging
from typing import Any
from typing import NoReturn
from typing import TypeVar

import fastapi
import pydantic
from httpx import Response
from cbra.ext.service import CurrentService
from cbra.ext.service import ServiceClient


M = TypeVar("M", bound=pydantic.BaseModel)


class ServiceRepository:
    """A repository implementation that uses an internal service as
    its data source.
    """
    __module__: str = 'libwebid.lib'

    #: The service client instance that is used to create HTTP requests
    #: to internal services.
    client: ServiceClient

    #: The default logger instance. Is assumed to log messages to stdout.
    logger: logging.Logger = logging.getLogger('uvicorn')

    #: The logical name of the resource.
    resource: str

    @classmethod
    def inject(cls) -> Any:
        return fastapi.Depends(cls)

    def __init__(
        self,
        client: ServiceClient = CurrentService
    ) -> None:
        self.client = client

    async def retrieve(
        self,
        resource_path: str,
        response_model: type[M] = M,
        params: dict[str, str] | None = None
    ) -> M | None:
        """Lookup the given resource and parse a successful response
        with the specified `response_model`. Return ``None`` if the
        HTTP status code of the response is ``404``, otherwise attempt
        to parse the error artifact enclosed in the response body and
        raise the appropriate exception.
        """
        if not str.startswith(resource_path, '/'):
            resource_path = f'/{resource_path}'
        response = await self.client.get(
            resource=self.resource,
            path=resource_path,
            params=params
        )
        if response.status_code == 404:
            return None
        elif response.status_code >= 400:
            await self.on_request_exception(response)
            assert False # nosec
        try:
            return response_model.parse_obj(response.json()) # type: ignore
        except pydantic.ValidationError:
            self.logger.exception(
                "Unexpected response format (resource: %s, path: %s)",
                self.resource, resource_path
            )
            raise
        except Exception:
            self.logger.exception(
                "Caught fatal %s while parsing response (resoure: %s, path: %s)",
                self.resource, resource_path
            )
            raise

    async def on_request_exception(self, response: Response) -> NoReturn:
        response.raise_for_status()
        raise NotImplementedError
