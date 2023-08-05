# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic

from .oauthclientdto import OAuthClientDTO


class AuthorizationRequestDTO(pydantic.BaseModel):
    client: OAuthClientDTO
    ui_locales: list[str] = []
    min_aal: int
    min_ial: int
    redirect_uri: str
    requests: list[str]
    acr_values: list[str] = []
    amr_values: list[str] = []

    def wants_amr(self, amr: str | set[str]) -> bool:
        """Return a boolean indicating if the request wants the given
        Authentication Method Reference (AMR).
        """
        if isinstance(amr, str):
            amr = {amr}
        return bool(set(self.amr_values) & amr)