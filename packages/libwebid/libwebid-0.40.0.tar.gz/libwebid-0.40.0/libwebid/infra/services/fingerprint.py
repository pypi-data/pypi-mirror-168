# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import logging

import httpx

from cbra.conf import settings
from cbra.exceptions import UpstreamServiceNotAvailable
from cbra.utils import retry
from cbra.utils import UpstreamExceptionRetryables
from libwebid.canon import Fingerprint
from libwebid.canon import FingerprintRef


ServiceFailure: UpstreamServiceNotAvailable = UpstreamServiceNotAvailable(5)

class FingerprintService:
    """Provides an interface to resolve fingerprints."""
    __module__: str = 'libwebid.infra.services'
    base_url: str
    api_key: str = getattr(settings, 'FINGERPRINTJS_API_KEY', '')
    logger: logging.Logger = logging.getLogger('uvicorn')

    def __init__(self, base_url: str = "https://api.fpjs.io"):
        self.base_url = base_url

    @retry(5, interval=2.0, only=UpstreamExceptionRetryables, exception=ServiceFailure)
    async def resolve(self, ref: FingerprintRef) -> Fingerprint:
        """Retrieve extended details for the given reference to a
        fingerprint.
        """
        headers = {'Auth-API-Key': self.api_key}
        async with httpx.AsyncClient(base_url=self.base_url, headers=headers) as client:
            response = await client.get( # type: ignore
                url=f'/visitors/{ref.visitor_id}',
                params={'request_id': ref.request_id}
            )
            if response.status_code in (400, 429):
                # 400 is assumed to occur when there is some tampering with the input,
                # 429 is rate limited.
                if response.status_code == 400:
                    self.logger.warning("Received 400 response from FingerprintJS")
                if response.status_code == 429:
                    self.logger.critical("FingerprintJS is rate-limiting requests.")
                raise ServiceFailure
            response.raise_for_status()
            data = response.json()
        visits = data.get('visits')
        if not visits:
            raise ServiceFailure
        return Fingerprint.parse_obj(visits[0])