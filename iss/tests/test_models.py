from django.test import TestCase
from django.core.management import call_command

from ..models import (CountryCode,
                      Organization)

import test_org

from membersuite_api_client.organizations.models import Organization as MSOrg
from membersuite_api_client.organizations.models import OrganizationType

from ..models import OrganizationType as OrgType
from ..membersuite import MemberSuiteSession


class CountryCodeTestCase(TestCase):

    def test_get_iso_country_code(self):
        """Does get_iso_country_code work?
        """
        country = CountryCode.objects.create(country_name='Erbania',
                                             iso_country_code='__')
        self.assertEqual('__', CountryCode.get_iso_country_code(
            country.country_name))

    def test_get_iso_country_code_missing_country(self):
        """Is get_iso_country_code resilient in the face of a missing country?
        """
        self.assertEqual('', CountryCode.get_iso_country_code(
            country_name='Sorry No Erbania Here'))


class MockMembersuiteAccount(object):

    def __init__(self, account_num, membersuite_id):
        self.organization = MSOrg(
            {"ID": account_num,
             "LocalID": membersuite_id,
             "Name": "AASHE Test Campus",
             "SortName": "AASHE Test Campus",
             "Mailing_Address": {
                 'CASSCertificationDate': None,
                 'CASSCertificationErrorMessage': None,
                 'CarrierRoute': None,
                 'City': 'Denver',
                 'Company': None,
                 'CongressionalDistrict': None,
                 'Country': 'US',
                 'County': None,
                 'DeliveryPointCheckDigit': None,
                 'DeliveryPointCode': None,
                 'GeocodeLat': '',
                 'GeocodeLong': '',
                 'LastGeocodeDate': '',
                 'Line1': '1536 Wynkoop St.',
                 'Line2': '',
                 'PostalCode': '80202',
                 'State': 'CO'
             },
             "WebSite": "",
             "Status": '6faf90e4-01f3-c54c-f01a-0b3bc87640ab',
             "Type": '11111111-1111-1111-1111-111111111111',
             "STARSCharterParticipant__c": "",
             "EmailAddress": "",
             }
        )


class OrganizationTestCase(TestCase):

    def setUp(self):
        self.country_code = CountryCode.objects.create(
            country_name='Joe', iso_country_code='__')
        self.org_type_data = {
            'ID': '11111111-1111-1111-1111-111111111111',
            'Name': 'Test Org Type'
        }
        self.org_type = OrganizationType(self.org_type_data)
        self.test_org_type = OrgType.upsert_org_type(self.org_type)
        self.matching_org = Organization.objects.create(
            account_num='6faf90e4-000b-c491-b60c-0b3c5398577c',
            membersuite_id=6044,
            org_name='AASHE Test Campus',
            picklist_name='AASHE Test Campus',
            street1='1536 Wynkoop St.',
            street2='',
            city='Denver',
            state='CO',
            country='US',
            postal_code='80202',
            country_iso=CountryCode.get_iso_country_code('US'),
            website='',
            is_defunct=False,
            org_type=self.test_org_type,
            stars_participant_status='',
            primary_email='',
            exclude_from_website=False,
        )
        self.matching_account = MockMembersuiteAccount(
            account_num='6faf90e4-000b-c491-b60c-0b3c5398577c',
            membersuite_id=6044
        )
        self.not_matching_account = MockMembersuiteAccount(
            account_num='6faf90e4-000b-c491-b60c-111111111111',
            membersuite_id=1111
        )
        self.mock_response = test_org.mock_response

    def test_get_organization_for_id(self):
        """Does get_organization_for_id work?
        """
        match = Organization.get_organization_for_id(
            self.matching_account.organization)
        self.assertEquals(self.matching_org.account_num,
                          match.account_num)

    def test_get_organization_for_id_no_match(self):
        """Is get_organization_for_id graceful when there's no match?
        """
        match = Organization.get_organization_for_id(
            self.not_matching_account.organization)
        self.assertEquals(None, match)

    def test_upsert_organization_insert(self):
        """Does upsert_for_account work when it needs to insert a record?
        """
        match = Organization.upsert_organization(
            self.not_matching_account.organization)
        self.assertEquals(self.not_matching_account.organization.account_num,
                          match.account_num)

    def test_upsert_organization_update(self):
        """Does upsert_for_account work when it needs to update a record?
        """
        new_membersuite_id = \
            self.matching_account.organization.membersuite_id + 1
        self.matching_account.organization.membersuite_id = new_membersuite_id
        match = Organization.upsert_organization(
            self.matching_account.organization
        )
        self.assertEquals(new_membersuite_id, match.membersuite_id)


class MembersuiteTestCase(TestCase):

    def test_membersuite_session(self):
        """Does instantiating MemberSuiteSession work?
        """
        session = MemberSuiteSession()
        self.assertTrue(session.session_id)
