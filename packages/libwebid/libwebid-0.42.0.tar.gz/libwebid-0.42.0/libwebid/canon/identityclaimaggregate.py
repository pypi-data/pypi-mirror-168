# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from collections import defaultdict
from typing import Any

import pydantic

from .conflictingclaim import ConflictingClaim
from .dateidentityclaim import DateIdentityClaim
from .identityclaimtype import IdentityClaimType
from .nameidentityclaim import NameIdentityClaim
from .officialgivennamesclaim import OfficialGivenNameIdentityClaim
from .stringidentityclaim import StringIdentityClaim


class IdentityClaimAggregate(pydantic.BaseModel):
    """Aggregates the claims from a sequence of :class:`IdentityClaim`
    instances.
    """
    given_name: OfficialGivenNameIdentityClaim | NameIdentityClaim | None = None
    family_name: NameIdentityClaim | None = None
    birthplace: StringIdentityClaim | None = None
    birthdate: DateIdentityClaim | None = None
    gender: StringIdentityClaim | None = None
    claims: list[IdentityClaimType] = []

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        for claim in self.claims:
            claim.contribute(self)

    def add(self, claim: IdentityClaimType) -> None:
        """Add the given `claim` to the aggregate."""
        for current in self.claims:
            if not current.can_compare(claim):
                continue
            if claim.conflicts(current):
                raise ValueError(f"Conflict between {current} and {claim}.")
        self.claims.append(claim)
        current = getattr(self, claim.name)
        if current is None or claim.supersedes(current):
            self.contribute(claim)

    def append(self, claimset: 'IdentityClaimAggregate') -> None:
        """Append the claims set to the existing claims."""
        for claim in claimset.claims:
            self.add(claim)

    def contribute(self, claim: IdentityClaimType) -> None:
        """Contributes :class:`IdentityClaim` to the currently aggregated
        value.
        """
        claim.contribute(self)

    def conflicts(self, claims: list[IdentityClaimType]) -> list[ConflictingClaim]:
        """Return the list of conflicts between the aggregated values
        and the claims provided in the list.
        """
        result: defaultdict[str, list[IdentityClaimType]] = defaultdict(list)
        for new in claims:
            for claim in new.get_compatible_claims():
                old = getattr(self, claim)
                if old is not None and new.conflicts(old):
                    result[new.name].append(new)
        return [
            ConflictingClaim(claim=getattr(self, old), conflicts=conflicts)
            for old, conflicts in result.items()
        ]

    def self_asserted(self) -> bool:
        """Return a boolean indicating if all claims in the aggregare are
        self-asserted.
        """
        return bool(self.claims and all([x.self_asserted() for x in self.claims]))

    def get_claims(self) -> dict[str, Any]:
        """Return a dictionary containing the claims."""
        return {k: v['value'] for k, v in self.dict(exclude={'claims'}).items()}