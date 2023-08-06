# Copyright (C) 2022 Cochise Ruhulessin
# 
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import fastapi
from cbra.ext.service import CurrentService
from cbra.ext.service import ServiceClient


class StorageEncrypter:
    __module__: str = 'libwebid.lib'
    _client: ServiceClient

    @classmethod
    def inject(cls) -> Any:
        return fastapi.Depends(cls)

    def __init__(self, svc: ServiceClient = CurrentService) -> None:
        self._client = svc

    async def decrypt(self, *args: Any, **kwargs: Any) -> Any:
        return await self._client.decrypt(*args, **kwargs)

    async def encrypt(self, data: Any, **kwargs: Any) -> str:
        return await self._client.encrypt(data=data, **kwargs)