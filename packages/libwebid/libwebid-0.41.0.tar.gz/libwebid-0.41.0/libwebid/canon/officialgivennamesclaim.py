# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Literal
from libwebid.canon.identificationartifacttype import IdentificationArtifactType

import pydantic
from libwebid.lib.i18n import gettext as _

from .identityclaim import IdentityClaim
from .identitydocumenttype import IdentityDocumentType
from .nameidentityclaim import NameIdentityClaim
from .multinameidentityclaim import MultiNameIdentityClaim


FrameworkType = Literal[
    IdentificationArtifactType.eherkenning,
    IdentificationArtifactType.eidas,
    IdentityDocumentType.driving_license,
    IdentityDocumentType.id_card,
    IdentityDocumentType.passport,
    IdentityDocumentType.permit,
]


class OfficialGivenNameIdentityClaim(MultiNameIdentityClaim):
    """The given names, as written on an official identity document, such as
    a passport or national identity card. These claims may contain one or
    more names, so special logic is required.
    """
    framework: FrameworkType = pydantic.Field(
        default=...,
        title=_("Framework"),
        description=_("The trust framework through which the claim was received.")
    )

    name: Literal['given_name'] = pydantic.Field(
        default='given_name',
        title=_("Name"),
        description=_("Is always `given_name`"),
        enum=['given_name',]
    )

    def as_initials(self) -> set[str]:
        return {x[0] for x in self.strip()}

    def conflicts(self, claim: IdentityClaim) -> bool:
        """Return a boolean indicating if the is a conflict between
        the claims.
        """
        if (self.name != 'given_name') or claim.name not in ('initials', 'given_name'):
            return super().conflicts(claim)
        conflicts = False
        if isinstance(claim, NameIdentityClaim):
            conflicts = not self.contains(claim)
        if isinstance(claim, OfficialGivenNameIdentityClaim):
            conflicts = not (
                self.strip() == claim.strip()
                or self.as_initials() == claim.as_initials()
            )
        return conflicts

    def is_official(self) -> bool:
        """Return a boolean indicating if the value was sourced from an official
        identity document, being a passport, national identity card or residence
        permit.
        """
        return True