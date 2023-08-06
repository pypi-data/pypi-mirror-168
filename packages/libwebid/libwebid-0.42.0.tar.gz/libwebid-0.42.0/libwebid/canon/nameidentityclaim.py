# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Literal

from .identityclaim import IdentityClaim
from .stringidentityclaim import StringIdentityClaim


class NameIdentityClaim(StringIdentityClaim):
    """A :class:`~libwebid.lib.IdentityClaim` implementation that
    represents a single name.
    """
    kind: Literal['name'] = 'name' # type: ignore

    def conflicts(self, claim: IdentityClaim) -> bool:
        """Return a boolean indicating if the is a conflict between
        the claims.
        """
        conflicts = False
        if claim.name == 'initials':
            value = str.lower(self.value[0])
            conflicts = value not in claim.strip()
        elif claim.is_official():
            conflicts = claim.conflicts(self)
        else:
            conflicts = super().conflicts(claim)
        return conflicts