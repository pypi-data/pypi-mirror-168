# Copyright (C) 2022 Cochise Ruhulessin
# 
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .repo.googledatastore import GoogleDatastoreRepository
from .localsubject import LocalSubject


class LocalSubjectRepository(GoogleDatastoreRepository):
    __module__: str = 'libwebid.lib'
    kind: str = 'LocalSubject'
    model: type[LocalSubject] = LocalSubject
    id_attr: str = 'ppid'

    async def get(self, subject_id: int) -> LocalSubject:
        return self.restore(await self.get_entity_by_id(subject_id))

    async def persist(self, obj: LocalSubject) -> LocalSubject:
        await self.persist_model(obj)
        return obj