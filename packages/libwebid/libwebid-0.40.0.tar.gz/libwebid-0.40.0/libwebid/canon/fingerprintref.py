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


class FingerprintRef(pydantic.BaseModel):
    """Represents a reference to a device fingerprint created with
    FingerprintJS.
    """
    request_id: str = pydantic.Field(
        default=...,
        title=_("Request ID")
    )

    visitor_id: str = pydantic.Field(
        default=...,
        title=_("Visitor ID")
    )