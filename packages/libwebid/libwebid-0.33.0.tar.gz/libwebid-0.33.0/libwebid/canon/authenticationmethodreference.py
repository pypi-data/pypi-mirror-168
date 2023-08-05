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
from ckms.utils import current_timestamp
from libwebid.lib.i18n import gettext as _


class AuthenticationMethodReference(pydantic.BaseModel):
    iss: str = pydantic.Field(
        default=...,
        title=_("Issuer"),
        description=_(
            "The entity that issued this Authentication Method "
            "Reference (AMR)."
        )
    )

    sub: int = pydantic.Field(
        default=...,
        title=_("Subject")
    )

    afr: int = pydantic.Field(
        default=...,
        title=_("Authentication Factor Reference (AFR)"),
        description=_(
            "Identifies the authentication factor that was used to "
            "create this reference."
        )
    )

    amr: Literal['otp'] = pydantic.Field(
        default=...,
        title=_("Authentication Method Reference (AMR)")
    )

    iat: int = pydantic.Field(
        default=...,
        title=_("Issued At"),
        description=_(
            "The date/time at which this AMR was created, in "
            "milliseconds since the UNIX epoch."
        )
    )

    exp: int = pydantic.Field(
        default=...,
        title=_("Issued At"),
        description=_(
            "The date/time at which this AMR expires, in "
            "milliseconds since the UNIX epoch. This value "
            "set by the issuer, consumer may implement their "
            "own criteria in accepting a signed AMR."
        )
    )

    def is_effective(self, max_age: int) -> bool:
        """Return a boolean indicating if the AMR is effective."""
        now = current_timestamp()
        return (now - max_age) <= self.iat