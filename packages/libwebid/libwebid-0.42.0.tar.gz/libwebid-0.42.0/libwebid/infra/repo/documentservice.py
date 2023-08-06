# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from libwebid.canon.api import documents
from libwebid.lib import ServiceRepository


class DocumentServiceRepository(ServiceRepository):
    __module__: str = 'libwebid.lib'
    resource: str = 'documents'

    async def get_session(
        self,
        session_id: int,
        with_pii: bool = False
    ) -> documents.RetrieveSessionResponse | None:
        params: dict[str, str] = {}
        if with_pii:
            params['pii'] = 'true'
        return await self.retrieve(
            resource_path=f'sessions/{session_id}',
            response_model=documents.RetrieveSessionResponse,
            params=params
        )