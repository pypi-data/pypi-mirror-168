# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os

#: The allows hosts that may make cross-origin requests.
API_BASE_DOMAIN: str = os.environ['API_BASE_DOMAIN']

APP_ENCRYPTION_KEY: str = 'enc'

APP_SIGNING_KEY: str = 'sig'

if 'FINGERPRINTJS_API_KEY' in os.environ:
    FINGERPRINTJS_API_KEY: str = os.environ['FINGERPRINTJS_API_KEY']

PII_ENCRYPTION_KEY: str = 'pii-enc'

PII_INDEX_KEY: str = 'pii-idx'

OAUTH2_SERVER: str = os.environ['OAUTH_SERVER']

OAUTH2_SERVICE_CLIENT: str = os.environ['OAUTH_SERVICE_CLIENT']