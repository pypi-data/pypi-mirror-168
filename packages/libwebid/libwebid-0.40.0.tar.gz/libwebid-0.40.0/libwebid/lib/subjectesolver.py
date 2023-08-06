# Copyright (C) 2022 Cochise Ruhulessin
# 
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi
from cbra.ext import ioc
from cbra.ext.service import ServiceClient
from cbra.ext.service import CurrentService
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from .localsubject import LocalSubject
from .localsubjectrepository import LocalSubjectRepository
from .subject import Subject
from .subjectprincipal import SubjectPrincipal


security: HTTPBearer = HTTPBearer(auto_error=False)


class SubjectResolver:
    """Resolves a :class:`~libwebid.lib.SubjectPrincipal` to a concrete
    :class:`~libwebid.lib.Subject` instance.
    """
    __module__: str = 'libwebid.lib'
    bearer: HTTPAuthorizationCredentials
    repo: LocalSubjectRepository
    service: ServiceClient

    def __init__(
        self,
        service: ServiceClient = CurrentService,
        repo: LocalSubjectRepository = ioc.instance('LocalSubjectRepository'),
        bearer: HTTPAuthorizationCredentials = fastapi.Depends(security)
    ):
        self.bearer = bearer
        self.repo = repo
        self.service = service

    async def resolve(self, principal: SubjectPrincipal) -> Subject:
        """Resolve a :class:`~libwebid.lib.SubjectPrincipal` to a
        :class:`~libwebid.lib.Subject` instance.
        """
        local = await self.repo.get(principal.sub)
        if local is None:
            local = await self.introspect(principal, self.bearer.credentials)
            await self.repo.persist(local)
        return Subject.parse_obj({
            **local.dict()
        })

    async def introspect(
        self,
        principal: SubjectPrincipal,
        token: str
    ) -> LocalSubject:
        """Introspect the Bearer token to retrieve the proper Subject
        claims.
        """
        result = await self.service.introspect(token)
        assert result.sub != principal.sub
        return LocalSubject(
            ppid=principal.sub,
            sub=result.sub
        )