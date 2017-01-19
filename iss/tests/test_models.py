from django.test import TestCase

from ..models import (CountryCode,
                      Organization)

import test_org


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
        self.account = {
            "ID": account_num,
            "LocalID": membersuite_id,
            "Name": "AASHE Test Campus",
            "SortName": "AASHE Test Campus",
            "Addresses": {
                'MemberSuiteObject': [
                    {
                        'ClassType': 'EntityAddress',
                        'Fields': {
                            'KeyValueOfstringanyType': [
                                {
                                    'Key': 'Type',
                                    'Value': '6faf90e4-000f-c013-958c-0b3bc8767dcd'
                                },
                                {
                                    'Key': 'Address',
                                    'Value': {
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
                                        'GeocodeLat': None,
                                        'GeocodeLong': None,
                                        'LastGeocodeDate': None,
                                        'Line1': '1536 Wynkoop St.',
                                        'Line2': None,
                                        'PostalCode': '80202',
                                        'State': 'CO'
                                    }
                                }
                            ]
                        }
                    }
                ]
            },
            "country_iso": CountryCode.get_iso_country_code('US'),
            "website": "",
            "is_defunct": "False",
            "org_type": "Four Year Institution",
            "stars_participant_status": "",
            "primary_email": "",
        }

class OrganizationTestCase(TestCase):

    def setUp(self):
        self.country_code = CountryCode.objects.create(
            country_name='Joe', iso_country_code='__')
        self.matching_org=Organization.objects.create(
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
            org_type='Four Year Institution',
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

    def test_get_organization_for_account(self):
        """Does get_organization_for_account work?
        """
        match = Organization.get_organization_for_account(
            self.matching_account.account)
        self.assertEquals(self.matching_org.account_num,
                          match.account_num)

    # def test_get_organization_for_account_no_match(self):
    #     """Is get_organization_for_account graceful when there's no match?
    #     """
    #     match = Organization.get_organization_for_account(
    #         self.not_matching_account)
    #     self.assertEquals(None, match)
    #
    # def test_get_organization_for_account_id(self):
    #     """Does get_organization_for_account_id work?
    #     """
    #     match = Organization.get_organization_for_account_id(
    #         self.matching_account.Id)
    #     self.assertEquals(self.matching_org.account_num,
    #                       match.account_num)
    #
    # def test_get_organization_for_account_id_no_match(self):
    #     """Is get_organization_for_account_id graceful when there's no match?
    #     """
    #     match = Organization.get_organization_for_account_id(
    #         self.not_matching_account.Id)
    #     self.assertEquals(None, match)
    #
    # def test_upsert_for_account_insert(self):
    #     """Does upsert_for_account work when it needs to insert a record?
    #     """
    #     match = Organization.upsert_for_account(self.not_matching_account)
    #     self.assertEquals(self.not_matching_account.Account_Number__c,
    #                       str(match.account_num))
    #
    # def test_upsert_for_account_update(self):
    #     """Does upsert_for_account work when it needs to update a record?
    #     """
    #     new_account_number = self.matching_account.Account_Number__c + '1'
    #     self.matching_account.Account_Number__c = new_account_number
    #     match = Organization.upsert_for_account(self.matching_account)
    #     self.assertEquals(new_account_number,
    #                       str(match.account_num))
