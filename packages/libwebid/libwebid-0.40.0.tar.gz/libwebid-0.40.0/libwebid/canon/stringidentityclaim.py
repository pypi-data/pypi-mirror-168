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

from .identityclaim import IdentityClaim


class StringIdentityClaim(IdentityClaim):
    value: str = pydantic.Field(
        default=...,
        title=_("Value"),
        description=_("The assertion content.")
    )

    @pydantic.validator('value', pre=True)
    def preprocess(
        cls,
        value: str | None
    ) -> str | None:
        if value is not None:
            value = str.strip(value)
        return value

    def strip(self) -> set[str]:
        """Strip the claim value of any characters that are not needed during
        comparison. Return a set contianing the sanitized value(s).
        """
        return {str.lower(self.value)}

    def conflicts(self, claim: IdentityClaim) -> bool:
        """Return a boolean indicating if the is a conflict between
        the claims.
        """
        return not isinstance(claim.value, str)\
            or str.lower(self.value) != str.lower(claim.value)