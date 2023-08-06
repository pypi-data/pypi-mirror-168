# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from gettext import gettext as _

import pydantic

from .authenticationmethodreference import AuthenticationMethodReference


class SessionClaims(pydantic.BaseModel):
    sub: int | None = pydantic.Field(
        default=None,
        title=_("Subject ID")
    )

    aal: int = pydantic.Field(
        default=1,
        title=_("Authentication Assurance Level (AAL)")
    )

    ial: int = pydantic.Field(
        default=1,
        title=_("Identity Assurance Level (AAL)")
    )

    allows_host: bool = pydantic.Field(
        default=False,
        title=_("Allows host?"),
        description=_(
            "Indicates if the connecting remote host is "
            "whitelisted for this session."
        )
    )

    allow_mfa_configuration: bool = pydantic.Field(
        default=False,
        title=_("Allow MFA configuration"),
        description=_(
            "Indicates if the session is allowed to configure MFA "
            "for the Subject it identifies."
        )
    )

    auth_time: int | None = pydantic.Field(
        default=None,
        title=_("Authenticated"),
        description=_(
            "The date/time at which the Subject was authenticated, "
            "in milliseconds since the UNIX epoch. If the session is not "
            "authenticated, this property shall be `null`."
        )
    )

    principal: int | None = pydantic.Field(
        default=None,
        title=_("Principal"),
        description=_(
            "The principal that was used to establish the session."
        )
    )

    email: str | None = pydantic.Field(
        default=None,
        title=_("Email"),
        description=(
            "The email address that was used to establish the session."
        )
    )

    email_verified: bool = pydantic.Field(
        default=False,
        title=_("Email verified?"),
        description=_(
            "Indicates if the email address of the authenticated Subject "
            "is verified."
        )
    )

    phone_verified: bool = pydantic.Field(
        default=False,
        title=_("Phonenumber verified?"),
        description=_(
            "Indicates if the phonenumber of the authenticated Subject "
            "is verified."
        )
    )

    scope: list[str] = pydantic.Field(
        default=["accounts.register"],
        title=_("Scope"),
        description=_("The authorization scope of the session.")
    )

    amr: dict[str, AuthenticationMethodReference] = pydantic.Field(
        default={},
        title="Authentication Methods References",
        description=_(
            "A mapping of strings representing `amr` values to JSON objects "
            "describing the authentication."
        )
    )

    uai: str | None = pydantic.Field(
        default=None,
        title=_("User-Agent Identifier (UAI)"),
        description=_(
            "A string identifying the user-agent that was used to "
            "visit the portal."
        )
    )

    incognito: bool = pydantic.Field(
        default=None,
        title=_("Incognito"),
        description=_(
            "Indicates if the session was established using an incognito "
            "user-agent."
        )
    )