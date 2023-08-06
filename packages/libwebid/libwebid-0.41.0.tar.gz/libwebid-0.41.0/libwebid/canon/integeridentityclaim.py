# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Literal

import pydantic
from libwebid.lib.i18n import gettext as _

from .identityclaim import IdentityClaim


class IntegerIdentityClaim(IdentityClaim):
    kind: Literal['integer'] = 'integer'

    value: int = pydantic.Field(
        default=...,
        title=_("Value"),
        description=_("The assertion content.")
    )

    def conflicts(self, claim: IdentityClaim) -> bool:
        """Return a boolean indicating if the is a conflict between
        the claims.
        """
        return not isinstance(claim.value, int)\
            or self.value != claim.value