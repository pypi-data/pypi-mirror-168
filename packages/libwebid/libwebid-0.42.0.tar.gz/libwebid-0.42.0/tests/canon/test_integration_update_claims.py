# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime

from libwebid.canon import BirthplaceIdentityClaim
from libwebid.canon import DateIdentityClaim
from libwebid.canon import GenderIdentityClaim
from libwebid.canon import IdentityClaimAggregate
from libwebid.canon import IdentityDocumentType
from libwebid.canon import NameIdentityClaim
from libwebid.canon import OfficialGivenNameIdentityClaim


def test_is_self_asserted():
    a1 = IdentityClaimAggregate(
        claims=[
            OfficialGivenNameIdentityClaim(
                name='given_name',
                framework=IdentityDocumentType.passport,
                value='Cochise Yri'
            ),
        ]
    )
    a2 = IdentityClaimAggregate(
        claims=[
            OfficialGivenNameIdentityClaim(
                name='given_name',
                framework=IdentityDocumentType.passport,
                value='Cochise Yri'
            ),
            NameIdentityClaim(
                name='family_name',
                value='Ruhulessin',
                source='documents/1'
            ),
        ]
    )
    a3 = IdentityClaimAggregate()
    assert a1.self_asserted()
    assert not a2.self_asserted()
    assert not a3.self_asserted()


def test_add_new_claim():
    a1 = IdentityClaimAggregate(
        claims=[
            OfficialGivenNameIdentityClaim(
                name='given_name',
                framework=IdentityDocumentType.passport,
                value='Cochise Yri'
            ),
        ]
    )
    a2 = IdentityClaimAggregate(
        claims=[
            NameIdentityClaim(name='family_name', value='Ruhulessin')
        ]
    )
    assert not a1.conflicts(a2.claims)


def test_can_serialize_and_deserialize_official_name():
    a1 = IdentityClaimAggregate(
        claims=[
            OfficialGivenNameIdentityClaim(
                name='given_name',
                framework=IdentityDocumentType.passport,
                value='Cochise Yri'
            ),
            NameIdentityClaim(name='family_name', value='Ruhulessin')
        ]
    )
    buf = a1.json()
    a2 = IdentityClaimAggregate.parse_raw(buf)
    assert isinstance(a2.given_name, OfficialGivenNameIdentityClaim)


def test_add_identity_document_to_self_asserted_claims():
    # The case when a user asserted its own identity with a
    # single first names, but has multiple official first names.
    # There should be no conflicts.
    a1 = IdentityClaimAggregate(
        claims=[
            NameIdentityClaim(name='given_name', value='Cochise'),
            NameIdentityClaim(name='family_name', value='Ruhulessin')
        ]
    )
    a2 = IdentityClaimAggregate(
        claims=[
            OfficialGivenNameIdentityClaim(
                name='given_name',
                framework=IdentityDocumentType.passport,
                value='Cochise Yri',
            ),
            NameIdentityClaim(name='family_name', value='Ruhulessin')
        ]
    )
    assert not a1.conflicts(a2.claims)


def test_single_name_asserted_with_partial_offical_does_not_conflict():
    a1 = IdentityClaimAggregate(
        claims=[
            NameIdentityClaim(name='given_name', value='Cochise'),
            NameIdentityClaim(name='family_name', value='Ruhulessin')
        ]
    )
    a2 = IdentityClaimAggregate(
        claims=[
            OfficialGivenNameIdentityClaim(
                name='given_name',
                framework=IdentityDocumentType.driving_license,
                value='Cochise Y'
            ),
            NameIdentityClaim(name='family_name', value='Ruhulessin')
        ]
    )
    assert not a1.conflicts(a2.claims)


def test_self_asserted_add_driving_license():
    a1 = IdentityClaimAggregate(
        claims=[
            NameIdentityClaim(
                name='given_name',
                framework=IdentityDocumentType.passport,
                value='Cochise'
            ),
            NameIdentityClaim(name='family_name', value='Ruhulessin')
        ]
    )
    a2 = IdentityClaimAggregate(
        claims=[
            OfficialGivenNameIdentityClaim(
                name='given_name',
                framework=IdentityDocumentType.passport,
                value='Cochise Y'
            ),
            NameIdentityClaim(name='family_name', value='Ruhulessin')
        ]
    )
    assert not a1.conflicts(a2.claims)


def test_self_asserted_add_driving_license_with_different_name():
    a1 = IdentityClaimAggregate(
        claims=[
            NameIdentityClaim(
                name='given_name',
                framework=IdentityDocumentType.passport,
                value='Cochise'
            ),
            NameIdentityClaim(name='family_name', value='Ruhulessin')
        ]
    )
    a2 = IdentityClaimAggregate(
        claims=[
            OfficialGivenNameIdentityClaim(
                name='given_name',
                framework=IdentityDocumentType.passport,
                value='Jan'
            ),
            NameIdentityClaim(name='family_name', value='Ruhulessin')
        ]
    )
    assert a1.conflicts(a2.claims)


def test_passport_add_driving_license_with_initial():
    a1 = IdentityClaimAggregate(
        claims=[
            OfficialGivenNameIdentityClaim(
                name='given_name',
                framework=IdentityDocumentType.passport,
                value='Cochise Yri'
            ),
            NameIdentityClaim(name='family_name', value='Ruhulessin')
        ]
    )
    a2 = IdentityClaimAggregate(
        claims=[
            OfficialGivenNameIdentityClaim(
                name='given_name',
                framework=IdentityDocumentType.passport,
                value='Cochise Y'
            ),
            NameIdentityClaim(name='family_name', value='Ruhulessin')
        ]
    )
    assert not a1.conflicts(a2.claims)


def test_passport_add_driving_license_with_different_initial():
    a1 = IdentityClaimAggregate(
        claims=[
            OfficialGivenNameIdentityClaim(
                name='given_name',
                framework=IdentityDocumentType.passport,
                value='Cochise Yri'
            ),
            NameIdentityClaim(name='family_name', value='Ruhulessin')
        ]
    )
    a2 = IdentityClaimAggregate(
        claims=[
            OfficialGivenNameIdentityClaim(
                name='given_name',
                framework=IdentityDocumentType.passport,
                value='Cochise Z'
            ),
            NameIdentityClaim(name='family_name', value='Ruhulessin')
        ]
    )
    assert a1.conflicts(a2.claims)


def test_single_name_asserted_with_partial_offical_does_conflict_on_different_names():
    a1 = IdentityClaimAggregate(
        claims=[
            OfficialGivenNameIdentityClaim(
                name='given_name',
                framework=IdentityDocumentType.passport,
                value='Cochise Yri'
            ),
            NameIdentityClaim(name='family_name', value='Ruhulessin')
        ]
    )
    a2 = IdentityClaimAggregate(
        claims=[
            NameIdentityClaim(name='given_name', value='Jan'),
            NameIdentityClaim(name='family_name', value='Ruhulessin')
        ]
    )
    conflicts = a1.conflicts(a2.claims)
    assert len(conflicts) == 1


def test_official_asserted_given_name_does_not_conflict_with_single_given_name():
    # The user has asserted its identity with an official document holding two
    # or more given names, and obtained additional identity assertions that
    # only state a single given name.
    a1 = IdentityClaimAggregate(
        claims=[
            OfficialGivenNameIdentityClaim(
                name='given_name',
                framework=IdentityDocumentType.passport,
                value='Cochise Yri'
            ),
            NameIdentityClaim(name='family_name', value='Ruhulessin')
        ]
    )
    a2 = IdentityClaimAggregate(
        claims=[
            NameIdentityClaim(name='given_name', value='Cochise'),
            NameIdentityClaim(name='family_name', value='Ruhulessin')
        ]
    )
    assert not a1.conflicts(a2.claims)


def test_single_name_asserted_with_different_official_name_conflicts():
    a1 = IdentityClaimAggregate(
        claims=[
            NameIdentityClaim(name='given_name', value='Cochise'),
            NameIdentityClaim(name='family_name', value='Ruhulessin')
        ]
    )
    a2 = IdentityClaimAggregate(
        claims=[
            OfficialGivenNameIdentityClaim(
                name='given_name',
                framework=IdentityDocumentType.passport,
                value='Jan'
            ),
            NameIdentityClaim(name='family_name', value='Ruhulessin')
        ]
    )
    conflicts = a1.conflicts(a2.claims)
    assert len(conflicts) == 1
    assert conflicts[0].claim.name == 'given_name'
    assert len(conflicts[0].conflicts) == 1
    assert conflicts[0].conflicts[0].name == 'given_name'
    assert conflicts[0].conflicts[0].value == 'Jan'


def test_update_asserted_identity_with_mismatching_official_document():
    a1 = IdentityClaimAggregate(
        claims=[
            NameIdentityClaim(name='given_name', value='Cochise'),
            NameIdentityClaim(name='family_name', value='Ruhulessin'),
            BirthplaceIdentityClaim(value='Amsterdam'),
            DateIdentityClaim(name='birthdate', value=datetime.date(1986, 5, 22)),
            GenderIdentityClaim(name='gender', value='male')
        ]
    )
    a2 = IdentityClaimAggregate(
        claims=[
            NameIdentityClaim(name='given_name', value='Jan'),
            NameIdentityClaim(name='family_name', value='de Boer'),
            BirthplaceIdentityClaim(value='Rotterdam'),
            DateIdentityClaim(name='birthdate', value=datetime.date(1990, 1, 1)),
            GenderIdentityClaim(name='gender', value='other')
        ]
    )
    conflicts = a1.conflicts(a2.claims)
    assert len(conflicts) == 5