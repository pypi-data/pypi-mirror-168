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


class FingerprintUseragent(pydantic.BaseModel):
    name: str | None = pydantic.Field(
        default=None,
        title=_("Name"),
        alias='browserName'
    )

    major_version: str | None = pydantic.Field(
        default=None,
        title=_("Major version"),
        alias='browserMajorVersion'
    )

    version: str | None = pydantic.Field(
        default=None,
        title=_("Version"),
        alias='browsbrowserFullVersionerMajorVersion'
    )

    os_name: str | None = pydantic.Field(
        default=None,
        title=_("OS Name"),
        alias='os'
    )

    os_version: str | None = pydantic.Field(
        default=None,
        title=_("OS Version"),
        alias='osVersion'
    )

    device: str | None = pydantic.Field(
        default=None,
        title=_("Device"),
        alias='device'
    )

    user_agent: str | None = pydantic.Field(
        default=None,
        title=_("User Agent"),
        alias='userAgent'
    )