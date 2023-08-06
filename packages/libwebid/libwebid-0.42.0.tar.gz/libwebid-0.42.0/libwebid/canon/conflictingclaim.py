# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic
from libwebid.lib.i18n import gettext as _

from .identityclaimtype import IdentityClaimType


class ConflictingClaim(pydantic.BaseModel):
    claim: IdentityClaimType = pydantic.Field(
        default=...,
        title=_("Claim"),
        description=_("The claim that caused a conflict.")
    )

    conflicts: list[IdentityClaimType] = pydantic.Field(
        default=...,
        title=_("Conflict"),
        description=_("The list of claims that are conflicted with.")
    )