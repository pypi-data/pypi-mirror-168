# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime
import secrets
from typing import Any

import pydantic


class SessionAssertion(pydantic.BaseModel):
    aal: int = 1
    allow_mfa_registration: bool = False
    auth_time: int
    challenge_id: int
    email: pydantic.EmailStr | None = None
    email_verified: bool = False
    exp: int = pydantic.Field(
        default_factory=lambda: (datetime.datetime.utcnow().timestamp() + 60)
    )
    ial: int = 1
    jti: str = pydantic.Field(default_factory=lambda: secrets.token_urlsafe(48))
    sub: int | None = None

    def dict(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        kwargs.setdefault('exclude_none', True)
        return super().dict(*args, **kwargs)

