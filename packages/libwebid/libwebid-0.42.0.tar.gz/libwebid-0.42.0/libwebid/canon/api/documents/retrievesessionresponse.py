# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic
from libwebid.canon import IdentityDocument
from libwebid.lib.i18n import gettext as _


class RetrieveSessionResponse(pydantic.BaseModel):
    subject_id: int = pydantic.Field(
        default=...,
        title=_("Subject ID"),
        description=_(
            "Identifies the Subject that initiated the identification "
            "session."
        )
    )

    status: str = pydantic.Field(
        default=...,
        title=_("Status"),
        description=_(
            "The current status of the identification session."
        )
    )

    session_url: str = pydantic.Field(
        default=...,
        title=_("Session URL"),
        description=_(
            "The URL that the user-agent may redirect to in order to "
            "retry the session."
        )
    )

    document: IdentityDocument | None = pydantic.Field(
        default=None,
        title="Document",
        description=_(
            "The identity document submitted to the session. Only present "
            "if `status` is `success`, otherwise `document` is `null`."
        )
    )