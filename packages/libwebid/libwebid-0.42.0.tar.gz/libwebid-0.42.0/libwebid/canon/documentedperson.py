# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime

import pydantic

from libwebid.lib.i18n import gettext as _


class DocumentedPerson(pydantic.BaseModel):
    """Represents a documented person i.e. whose identity is
    assert by a document that was issued by a recognized
    entity.
    """
    given_names: str = pydantic.Field(
        default=...,
        title=_("Given name(s)"),
        description=_(
            "The given name(s) of the person. This property contains one "
            "or more names, depending on the type of document that was used."
        )
    )

    last_name: str = pydantic.Field(
        default=...,
        title=_("Last name"),
        description=_("The last name (family name) of the person.")
    )

    birthdate: datetime.date = pydantic.Field(
        default=...,
        title="Birthdate"
    )

    ncn: str = pydantic.Field(
        default=None,
        title=_("National Citizen Number (NCN)"),
        description=_(
            "The government-issued citizen number, such as the "
            "Burgerservicenummer (BSN)."
        )
    )