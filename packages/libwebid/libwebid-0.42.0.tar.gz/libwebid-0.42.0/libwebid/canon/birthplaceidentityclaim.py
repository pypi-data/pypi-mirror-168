# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import re
from typing import Literal

import pydantic
from libwebid.lib.i18n import gettext as _

from .stringidentityclaim import StringIdentityClaim


class BirthplaceIdentityClaim(StringIdentityClaim):
    kind: Literal['locality'] = 'locality'
    name: Literal['birthplace'] = pydantic.Field(
        default='birthplace',
        title=_("Birthplacce"),
        description=_("Is always `birthplace`"),
        enum=['birthplace']
    )

    def strip(self) -> set[str]:
        stripped = {str.lower(x) for x in re.split('\\s+', self.value)}
        return {x for x in stripped }