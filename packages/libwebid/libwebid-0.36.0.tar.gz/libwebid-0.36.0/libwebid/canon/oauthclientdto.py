# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic

from .oauthclientaccesstype import OAuthClientAccessType


class OAuthClientDTO(pydantic.BaseModel):
    client_id: int | str
    organization_id: int
    organization_name: str
    display_name: str
    first_party: bool
    access: OAuthClientAccessType
    min_ial: int = 0
    min_aal: int = 0