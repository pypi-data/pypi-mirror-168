# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime
from typing import Any

from libwebid.canon import TokenConsumed
from libwebid.domain import TokenRepository
from libwebid.lib.repo.googledatastore import GoogleDatastoreRepository


class DatastoreTokenRepository(TokenRepository, GoogleDatastoreRepository):
    kind: str = 'Token'

    async def consume(self, token: Any) -> None:
        entity = await self.get_entity_by_id(token.jti)
        if entity is not None:
            raise TokenConsumed
        entity = self.entity_factory(token.jti)
        entity.update({ # type: ignore
            'exp': datetime.datetime.fromtimestamp(token.exp)
        }) 
        await self.put(entity)
