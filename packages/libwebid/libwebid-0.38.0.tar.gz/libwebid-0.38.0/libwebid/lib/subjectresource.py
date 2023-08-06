# Copyright (C) 2022 Cochise Ruhulessin
# 
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Callable

import fastapi
from cbra.conf import settings
from cbra.ext.oauth2 import RFC9068Principal
from cbra.resource import Resource
from .subject import Subject
from .subjectprincipal import SubjectPrincipal
from .subjectesolver import SubjectResolver


class SubjectResource(Resource):
    """A :class:`cbra.resource.Resource` implementation that authenticates
    the Subject with an :rfc:`9068` access token.
    """
    __abstract__: bool = True
    __module__: str = 'libwebid.lib'
    principal: SubjectPrincipal
    principal_factory: Any = RFC9068Principal(
        principal_factory=SubjectPrincipal.fromclaimset,
        trusted_issuers=getattr(settings, 'TRUSTED_ISSUERS', None) or set()
    )
    resolver: SubjectResolver = fastapi.Depends(SubjectResolver)
    subject: Subject

    async def resolve_subject(
        self,
        resolver: SubjectResolver = fastapi.Depends()
    ) -> None:
        self.subject = await resolver.resolve(self.principal)

    def get_dependants(self) -> list[Callable[..., Any]]:
        dependants = super().get_dependants()
        dependants.append(self.resolve_subject)
        return dependants