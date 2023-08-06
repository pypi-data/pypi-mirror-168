# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pytest

from libwebid.canon import NameIdentityClaim
from libwebid.canon import MultiNameIdentityClaim



@pytest.mark.parametrize("c1", [
    NameIdentityClaim(name='given_name', value='Cochise')
])
@pytest.mark.parametrize("c2", [
    NameIdentityClaim(name='given_name', value='cochise'),
    NameIdentityClaim(name='given_name', value='COCHISE'),
    NameIdentityClaim(name='given_name', value='COCHISE '),
])
def test_name_is_case_insensitive(
    c1: MultiNameIdentityClaim,
    c2: MultiNameIdentityClaim
):
    assert not c1.conflicts(c2)



@pytest.mark.parametrize("c1", [ # type: ignore
    MultiNameIdentityClaim(name='given_name', value="Cochise Yri")
])
@pytest.mark.parametrize("c2", [ # type: ignore
    MultiNameIdentityClaim(name='given_name', value="Cochise yri"),
    MultiNameIdentityClaim(name='given_name', value="cochise yri"),
    MultiNameIdentityClaim(name='given_name', value="CoChIsE yRi"),
    MultiNameIdentityClaim(name='given_name', value="COCHISE YRI"),
    MultiNameIdentityClaim(name='given_name', value="COCHISE YRI "),
])
def test_multiname_is_case_insensitive(
    c1: MultiNameIdentityClaim,
    c2: MultiNameIdentityClaim
):
    assert not c1.conflicts(c2)


def test_name_conflicts_multiname():
    c1 = NameIdentityClaim(name='given_name', value='cochise')
    c2 = MultiNameIdentityClaim(name='given_name', value='Cochise Yri')
    assert c1.conflicts(c2)


def test_multiname_contains_name():
    c1 = NameIdentityClaim(name='given_name', value='cochise')
    c2 = MultiNameIdentityClaim(name='given_name', value='Cochise Yri')
    assert c1.is_contained_by(c2)
    assert c2.contains(c1), f'{c1.strip()} <= {c2.strip()}'