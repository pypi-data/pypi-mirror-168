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
from typing import Callable

import pydantic
from libwebid.lib.i18n import gettext as _

from .identificationartifacttype import IdentificationArtifactType
from .identitydocumenttype import IdentityDocumentType


class IdentityClaim(pydantic.BaseModel):
    """Represents an assertion about the identity of a natural
    person.
    """
    kind: str

    name: str = pydantic.Field(
        default=...,
        title=_("Name"),
        description=_(
            "The name of data-element that is asserted regarding the "
            "subject."
        ),
        enum=[
            'birthdate',
            'birthplace',
            'family_name',
            'gender',
            'given_name',
            'initials'
            'name',
        ]
    )

    value: int | str | datetime.date = pydantic.Field(
        default=...,
        title=_("Value"),
        description=_("The assertion content.")
    )

    ial: int = pydantic.Field(
        default=1,
        title=_("Identity Assurance Level (IAL)"),
        description=_(
            "Indicates the confidence given by the server in this specific "
            "claim."
        )
    )

    framework: IdentificationArtifactType | IdentityDocumentType = pydantic.Field(
        default=IdentificationArtifactType.asserted,
        title=_("Framework"),
        description=_("The trust framework through which the claim was received."),
    )

    source: str = pydantic.Field(
        default='self',
        title=_("Source"),
        description=_(
            "Identifies the source of the claim. Is `self` for self-asserted "
            "claims, `composite` for an aggregration of claims, and otherwise "
            "an URI pointing to an `IdentityDocument` or `IdentificationArtifact`."
        )
    )

    asserted: datetime.datetime = pydantic.Field(
        default_factory=lambda: datetime.datetime.utcnow().replace(second=0, microsecond=0),
        title=_("Asserted"),
        description=_(
            "The date/time at which this claim was asserted by the source."
        )
    )

    @pydantic.validator('asserted')
    def preprocess_asserted(
        cls,
        value: datetime.datetime
    ) -> datetime.datetime:
        return value.replace(second=0, microsecond=0)

    def can_compare(self, claim: 'IdentityClaim'):
        """Return a boolean indicating if the claims can be compared."""
        return claim is not None and (self.name == claim.name)

    def conflicts(self, claim: 'IdentityClaim') -> bool:
        """Return a boolean indicating if the is a conflict between
        the claims.
        """
        raise NotImplementedError

    def contains(self, claim: 'IdentityClaim') -> bool:
        """Return a boolean indicating if the given claim is contained by
        this claim.
        """
        return claim.is_contained_by(self)

    def contribute(
        self,
        obj: Any,
        setter: Callable[[Any, str, 'IdentityClaim'], Any] = setattr
    ) -> None:
        """Contribute the claim to `obj` using `setter`."""
        setter(obj, self.name, self)

    def get_compatible_claims(self) -> list[str]:
        """Return the list of compatible claims."""
        return [self.name]

    def is_contained_by(self, claim: 'IdentityClaim') -> bool:
        """Return a boolean indicating if the given claim contains
        this claim.
        """
        return self.strip() <= claim.strip()

    def is_official(self) -> bool:
        """Return a boolean indicating if the value was sourced from an official
        identity document, being a passport, national identity card or residence
        permit.
        """
        return False

    def is_superseded(self, claim: 'IdentityClaim') -> bool:
        """Return a boolean indicating if this claim is superseded
        the given `claim`.
        """
        return claim.supersedes(self)

    def self_asserted(self) -> bool:
        """Return a boolean indicating if the claim is self-asserted."""
        return self.source == 'self'

    def strip(self) -> set[Any]:
        """Strip the claim value of any characters that are not needed during
        comparison. Return a set containing the sanitized value(s).
        """
        raise NotImplementedError

    def supersedes(self, claim: 'IdentityClaim') -> bool:
        """Return a boolean indicating if this claim supersedes
        the given `claim`.
        """
        return (self.ial == claim.ial) and (self.asserted > claim.asserted)\
            or self.ial > claim.ial

    def __lt__(self, claim: 'IdentityClaim') -> bool:
        return self.is_superseded(claim)

    def __gt__(self, claim: 'IdentityClaim') -> bool:
        return self.supersedes(claim)