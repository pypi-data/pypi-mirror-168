# Copyright (C) 2022 Cochise Ruhulessin
# 
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from cbra.conf import settings
from cbra.ext.oauth2 import RFC9068Principal
from cbra.resource import Resource
from .serviceprincipal import ServicePrincipal


if hasattr(settings, 'OAUTH2_SERVICE_ISSUER'):
    TRUSTED_ISSUERS: set[str] = {f"{getattr(settings, 'OAUTH2_SERVICE_ISSUER')}"}
else:
    TRUSTED_ISSUERS: set[str] = set() # type: ignore


class ServiceResource(Resource):
    """A :class:`cbra.resource.Resource` implementation that authenticates
    a service with an :rfc:`9068` access token.
    """
    __abstract__: bool = True
    __module__: str = 'libwebid.lib'
    principal: ServicePrincipal
    principal_factory: Any = RFC9068Principal(
        principal_factory=ServicePrincipal.fromclaimset,
        trusted_issuers=TRUSTED_ISSUERS
    )
