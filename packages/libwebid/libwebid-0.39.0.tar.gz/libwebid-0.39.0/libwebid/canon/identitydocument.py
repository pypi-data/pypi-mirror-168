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

import iso3166
from libwebid.lib.i18n import gettext as _

from .documentedperson import DocumentedPerson
from .identitydocumenttype import IdentityDocumentType


class IdentityDocument(pydantic.BaseModel):
    """Represents a document that identifies a person, such as a
    passport or national identity card.
    """
    document_type: IdentityDocumentType = pydantic.Field(
        default=...,
        title=_("Document type"),
        description=_("Indicates the type of document.")
    )

    country: str = pydantic.Field(
        default=...,
        title=_("Issueing country"),
        description=_(
            "An ISO 3166 numeric country code identifying the country "
            "that issued the official document. If the document was "
            "issued by a non-state actor that is a recognized authority,"
            "`country` has the value of `999`."
        )
    )

    number: str = pydantic.Field(
        default=...,
        title=_("Document number"),
        description=_(
            "The document number as assigned by the issuer."
        )
    )

    valid_from: datetime.date = pydantic.Field(
        default=...,
        title=_("Valid from"),
        description=_(
            "The date from which the document is valid."
        )
    )

    valid_until: datetime.date = pydantic.Field(
        default=...,
        title=_("Valid until"),
        description=_(
            "The date until which the document is valid."
        )
    )

    person: DocumentedPerson = pydantic.Field(
        default=...,
        title=_("Documented person"),
        description=_(
            "The person that is documented by this identity document."
        )
    )

    @pydantic.validator('country', pre=True)
    def preprocess_country(
        cls,
        value: str | None
    ) -> str | None:
        if isinstance(value, str) and len(value) in (2, 3):
            try:
                country = iso3166.countries.get(value) # type: ignore
            except KeyError:
                raise ValueError(f'Invalid ISO-3166 code: {value}')
            value = country.numeric
        elif isinstance(value, str):
            raise ValueError(f'Not an ISO-3166 code: {value}')
        return value

    def is_valid(self) -> bool:
        """Return a boolean indicating if the document is valid,
        based on :attr:`valid_until`.
        """
        return self.valid_until < datetime.date.today()