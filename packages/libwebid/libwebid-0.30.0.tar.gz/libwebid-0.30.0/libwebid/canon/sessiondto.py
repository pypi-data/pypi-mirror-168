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
        if max_age is not None:
            raise NotImplementedError
        if isinstance(amr, str):
            amr = {amr}
        return bool(set(self.claims.amr) & amr)