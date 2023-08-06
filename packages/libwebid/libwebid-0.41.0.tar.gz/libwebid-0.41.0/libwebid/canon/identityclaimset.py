# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime
from typing import Literal

import pydantic


class IdentityClaimSet(pydantic.BaseModel):
    name: str | None = pydantic.Field(
        default=None,
        title="Name",
        description=(
            "Subject full name in displayable form including all name "
            "parts, possibly including titles and suffixes, ordered "
            "according to the Subject's locale and preferences."
        )
    )

    given_name: str | None = pydantic.Field(
        default=None,
        title="Given name",
        description=(
            "Given name(s) or first name(s) of the End-User. Note that "
            "in some cultures, people can have multiple given names; "
            "all can be present, with the names being separated by "
            "space characters."
        )
    )

    family_name: str | None = pydantic.Field(
        default=None,
        title="Family name",
        description=(
            "Surname(s) or last name(s) of the End-User. Note that in some cultures, "
            "people can have multiple family names or no family name; all can be "
            "present, with the names being separated by space characters."
        )
    )

    birthdate: datetime.date | None = pydantic.Field(
        default=None,
        title="Birthdate",
        description=(
            "End-User's birthday, represented as an ISO 8601:2004 YYYY-MM-DD "
            "format. The year MAY be 0000, indicating that it is omitted. "
            "To represent only the year, YYYY format is allowed. Note that "
            "depending on the underlying platform's date related function, "
            "providing just year can result in varying month and day, so "
            "the implementers need to take this factor into account to "
            "correctly process the dates."
        )
    )

    birthplace: str | None = pydantic.Field(
        default=None,
        title="Birthplace",
        description=(
            "End-Users's place of birth, without the country name."
        )
    )

    gender: Literal['male', 'female', 'other'] | None = pydantic.Field(
        default=None,
        title="Gender",
        description=(
            "The gender of the subject. May be `male`, `female`, or "
            "`other`."
        )
    )

    ial: int = pydantic.Field(
        default=1,
        title="Identity Assurance Level (IAL)",
        description=(
            "Indicates the confidence that the server has in the asserted "
            "identity claims (`given_name`, `family_name`, `gender`, "
            "`birthdate` and `birthplace`)."
        )
    )


    def diff(self, claims: 'IdentityClaimSet') -> list[str]:
        """Return the list of field names that have changed with respect
        to the claims.
        """
        fields = ['given_name', 'family_name', 'gender', 'birthdate', 'birthplace']
        changed: list[str] = []
        for field in fields:
            if self.compare_field(claims, field):
                continue
            changed.append(field)
        return changed

    def update(self, claims: 'IdentityClaimSet', force: bool = False) -> None:
        if claims.ial > self.ial:
            self.ial = claims.ial
        self.update_claim('given_name', claims, force)
        self.update_claim('family_name', claims, force)
        self.update_claim('birthdate', claims, force)
        self.update_claim('birthplace', claims, force)
        self.update_claim('gender', claims, force)

    def update_claim(
        self,
        name: str,
        claims: 'IdentityClaimSet',
        force: bool = False
    ) -> None:
        """Update the claim of the given `name` from the :class:`IdentityClaimSet`
        `claims`.

        If the current value of the claim is ``None``, then update the claim;
        otherwise ensure that the values are equal.
        """
        old = getattr(self, name)
        new = getattr(claims, name)
        if old is None:
            setattr(self, name, new)
            return
        is_equal = (old == new)\
            if not isinstance(new, str)\
            else (str.lower(old) == str.lower(new))
        if not is_equal and not force:
            raise Exception

    def compare_field(self, claims: 'IdentityClaimSet', field: str) -> bool:
        """Compares the given field with the other claimset."""
        old = getattr(self, field)
        new = getattr(claims, field)
        if isinstance(new, str):
            new = str.lower(new)
        if isinstance(old, str):
            old = str.lower(old)
        return (old == new)