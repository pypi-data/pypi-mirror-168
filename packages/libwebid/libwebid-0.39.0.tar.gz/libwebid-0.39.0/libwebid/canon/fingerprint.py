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

from .fingerprintconfidence import FingerprintConfidence
from .fingerprintlocation import FingerprintLocation
from .fingerprintuseragent import FingerprintUseragent


class Fingerprint(pydantic.BaseModel):
    """Represents a reference to a device fingerprint created with
    FingerprintJS.
    """
    request_id: str = pydantic.Field(
        default=...,
        title=_("Request ID"),
        alias='requestId'
    )

    incognito: bool = pydantic.Field(
        default=False,
        title=_("Incognito?")
    )

    ip: str = pydantic.Field(
        default=...,
        title=_("IPv4 Address")
    )

    location: FingerprintLocation | None = pydantic.Field(
        default=None,
        title=_("Location"),
        alias='ipLocation'
    )

    ua: FingerprintUseragent | None = pydantic.Field(
        default=None,
        title=_("User Agent"),
        alias='browserDetails'
    )

    confidence: FingerprintConfidence = pydantic.Field(
        default=...,
        title=_("Confidence")
    )

    url: str = pydantic.Field(
        default=...,
        title=_("URL")
    )

    timestamp: int = pydantic.Field(
        default=...,
        title=_("Timestamp")
    )