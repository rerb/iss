from django.test import TestCase
import datetime

from ..models import (CountryCode, Organization, Membership,
                      OrganizationType, MembershipProduct)

import test_org

from membersuite_api_client.organizations.models import Organization as MSOrg
from membersuite_api_client.memberships.models import Membership as MSMember
from membersuite_api_client.memberships.models import MembershipProduct \
    as MSMemProduct
from membersuite_api_client.organizations.models import OrganizationType \
    as MSOrgType

from ..membersuite import MemberSuiteSession
from ..utils import upsert_org_types, \
                    upsert_organizations, \
                    upsert_membership_products, upsert_memberships, \
                    upsert_membership_ownerships


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
             "SalesforceID__c": None,
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
        self.membership = MSMember(
            {"ID": '22222222-2222-2222-2222-222222222222',
             "Owner": account_num,
             "MembershipDirectoryOptOut": False,
             "ReceivesMemberBenefits": True,
             "CurrentDuesAmount": "1.0",
             "ExpirationDate": datetime.datetime.now() +
                               datetime.timedelta(days=1),
             "Product": '99999999-9999-9999-9999-999999999999',
             "Type": '6faf90e4-006a-c1e7-1ac8-0b3c2f7cb3bc',
             "LastModifiedDate": datetime.datetime.now()-datetime.timedelta(
                 days=1),
             "Status": '6faf90e4-0069-c2ef-6d51-0b3c15a7cb7f',
             "JoinDate": datetime.datetime.now()+datetime.timedelta(days=-2),
             "TerminationDate": None,
             "RenewalDate": datetime.datetime.now()+datetime.timedelta(days=-1)
             }
        )


class OrganizationTestCase(TestCase):

    def setUp(self):
        self.country_code = CountryCode.objects.create(
            country_name='Joe', iso_country_code='__')
        
        # Set up an Organization Type
        self.org_type_data = {
            'ID': '11111111-1111-1111-1111-111111111111',
            'Name': 'Test Org Type'
        }
        self.org_type = MSOrgType(self.org_type_data)
        self.test_org_type = OrganizationType.upsert_org_type(self.org_type)

        # Set up a Membership Product
        self.product_data = {
            "ID": '99999999-9999-9999-9999-999999999999',
            "Name": 'Super Awesome Mega Membership'
        }
        self.product = MSMemProduct(self.product_data)
        self.membership_product = MembershipProduct.objects.create(
            id='99999999-9999-9999-9999-999999999999',
            name='Super Awesome Mega Membership'
        )
        
        # Set up an Organization based on AASHE Test Campus object
        self.matching_org = Organization.objects.create(
            account_num='6faf90e4-000b-c491-b60c-0b3c5398577c',
            membersuite_id=6044,
            salesforce_id=None,
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
        self.no_membersuite_id_account = MockMembersuiteAccount(
            account_num=None,
            membersuite_id=None
        )
        self.no_membersuite_id_org = Organization.objects.create(
            account_num=None,
            membersuite_id=None,
            salesforce_id="111111",
            org_name='No Membersuite ID Org',
            picklist_name='No Membersuite ID Org',
            street1='',
            street2='',
            city='',
            state='',
            country='',
            postal_code='',
            country_iso=CountryCode.get_iso_country_code('US'),
            website='',
            is_defunct=False,
            org_type=self.test_org_type,
            stars_participant_status='',
            primary_email='',
            exclude_from_website=False,
        )

        # Set up a Membership
        self.membership = Membership.objects.create(
            id='22222222-2222-2222-2222-222222222222',
            owner=Organization.get_organization_for_id(
                self.matching_account.organization),
            receives_membership_benefits=True,
            status='Renewed',
            membership_directory_opt_out=False,
            join_date=datetime.datetime.now() + datetime.timedelta(days=-1),
            expiration_date=datetime.datetime.now() + datetime.timedelta(
                days=1),
            last_modified_date=datetime.datetime.now() +
                               datetime.timedelta(days=-1),
            product=self.membership_product
        )

        self.mock_response = test_org.mock_response

    def test_get_org_type_for_id(self):
        """Does get_org_type_for_id work?
        """
        match = OrganizationType.get_org_type_for_id(self.org_type)
        self.assertEqual(match.name, 'Test Org Type')

    def test_upsert_org_type(self):
        # Should already exist in test DB
        match = OrganizationType.objects.get(
            id='11111111-1111-1111-1111-111111111111')
        self.assertEqual(match.name, 'Test Org Type')

        # Now change the name and upsert
        self.org_type.name = 'New Org Type'
        match = OrganizationType.upsert_org_type(self.org_type)
        match = OrganizationType.objects.get(
            id='11111111-1111-1111-1111-111111111111')
        self.assertEqual(match.name, 'New Org Type')

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

    def test_upsert_organization_update_by_salesforce_id(self):
        """Does this correctly update a record if it has no MemberSuite ID
           but already has a SalesForce entry?
        """
        # Check that setUp created the org we need correctly
        match = Organization.objects.get(salesforce_id="111111")
        self.assertEqual(match.org_name, 'No Membersuite ID Org')
        self.assertFalse(match.account_num)
        self.assertFalse(match.membersuite_id)

        # Now restore those values to the "matching account" and upsert again.
        # It should update the record in place, so get should still return 1.
        self.no_membersuite_id_account.organization.extra_data[
            "SalesforceID__c"] = "111111"
        self.no_membersuite_id_account.organization.membersuite_id = 9999
        self.no_membersuite_id_account.organization.account_num = 'asdf'
        org = Organization.upsert_organization(
            self.no_membersuite_id_account.organization)

        match = Organization.objects.get(salesforce_id="111111")
        self.assertEqual(match.org_name, 'AASHE Test Campus')
        self.assertEqual(match.membersuite_id, 9999)
        self.assertEqual(match.account_num, 'asdf')

    def test_upsert_utils(self):
        """Do the upsert commands within utils.py work
        """
        upsert_org_types()
        qs = OrganizationType.objects.all()
        # If the upsert command worked, we will have OrgType objects present
        self.assertTrue(qs)

        upsert_membership_products()
        qs = MembershipProduct.objects.all()
        # If the upsert command worked, we will have MembershipProduct objects

        upsert_organizations(since=1, get_all=False)
        upsert_memberships(since=1, get_all=False)
        """ I don't even think there's a test we can do here. At best, once we
        have a sandbox, we can test that it updates zero rows, but for now we
        just run the command to see that no errors occur. If something goes
        wrong, the build will fail and we will be see that it occurred here.
        """

        # Test upserting Membership-Org ownership relationships
        upsert_membership_ownerships()
        org = Organization.objects.get(membersuite_id=6044)
        self.assertTrue(org.is_member)

    def test_upsert_membership_product_insert(self):
        """Does upsert_membership_product work?
        """
        self.product.name = 'New Product Name'
        product = MembershipProduct.upsert_membership_product(self.product)
        match = MembershipProduct.objects.get(
            id='99999999-9999-9999-9999-999999999999')
        self.assertEqual(match.name, 'New Product Name')

    def test_upsert_membership_product_update(self):
        """Does upsert_membership_product work?
        """
        # Product should already exist in the test db from setUp()
        match = MembershipProduct.objects.get(
            id='99999999-9999-9999-9999-999999999999')
        self.assertEqual(match.name, 'Super Awesome Mega Membership')

        # Now change the name of it and upsert
        self.product.name = 'New Product Name'
        product = MembershipProduct.upsert_membership_product(self.product)
        match = MembershipProduct.objects.get(
            id='99999999-9999-9999-9999-999999999999')
        self.assertEqual(match.name, 'New Product Name')

    def test_get_product_for_id(self):
        """Does get_product_for_id work?
        """
        match = MembershipProduct.get_product_for_id(self.product)
        self.assertEqual(match.name, 'Super Awesome Mega Membership')

    def test_get_membership_for_id(self):
        """Does get_membership_for_id work?
        """
        match = Membership.get_membership_for_id(
            self.matching_account.membership)
        self.assertEquals(match.id, '22222222-2222-2222-2222-222222222222')

    def test_upsert_membership_insert(self):
        """Does upsert_membership work when inserting a new object?
        """
        Membership.upsert_membership(self.matching_account.membership)
        match = Membership.objects.get(
            id='22222222-2222-2222-2222-222222222222'
        )
        self.assertTrue(match)

    def test_upsert_membership_update(self):
        """Does upsert_membership work when updating an existing object?
        """
        # Should already exist and confirm field value is true to begin with
        match = Membership.objects.get(
            id='22222222-2222-2222-2222-222222222222')
        self.assertTrue(match.receives_membership_benefits)

        # now update it
        self.matching_account.membership.receives_member_benefits = False
        Membership.upsert_membership(self.matching_account.membership)
        match = Membership.objects.get(
            id='22222222-2222-2222-2222-222222222222')
        self.assertFalse(match.receives_membership_benefits)


class MembersuiteTestCase(TestCase):

    def test_membersuite_session(self):
        """Does instantiating MemberSuiteSession work?
        """
        session = MemberSuiteSession()
        self.assertTrue(session.session_id)
