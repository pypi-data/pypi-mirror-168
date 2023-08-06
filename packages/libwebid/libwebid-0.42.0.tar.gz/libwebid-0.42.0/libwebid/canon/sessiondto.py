# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import pydantic

from .sessionclaims import SessionClaims


class SessionDTO(pydantic.BaseModel):
    tasks: list[Any]
    claims: SessionClaims

    def has_amr(self, amr: str | set[str], max_age: int | None = None) -> bool:
        """Return a boolean if the session has the specified Authentication
        Method Reference(s) (AMR).
        """
        if isinstance(amr, str):
            amr = {amr}
        has_required_methods = bool(amr <= set(self.claims.amr))
        if not has_required_methods:
            return False
        if max_age:
            for type in amr:
                ref = self.claims.amr[type]
                if not ref.is_effective(max_age):
                    has_required_methods = False
                    break
        return has_required_methods