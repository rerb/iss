from django.test import TestCase

from ..models import (CountryCode,
                      Organization)


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


class MockSalesforceAccount(object):

    def __init__(self, Account_Number__c=0, Id=0, BillingCountry=None):
        self.Id = Id
        self.Account_Number__c = str(Account_Number__c)

        self.Name = 'Default Account Name'
        self.picklist_name__c = 'Default Picklist Name'
        self.BillingStreet = ''
        self.BillingCity = ''
        self.BillingState = ''
        self.BillingCountry = BillingCountry
        self.BillingPostalCode = ''
        self.Website = ''
        self.Sustainability_website__c = ''
        self.Carnegie_Classification__c = ''
        self.Carnegie_2005_Enrollment_Profile_Text__c = ''
        self.FTE_Enrollment_All_Degrees__c = 0
        self.Latitude__c = 0
        self.Longitude__c = 0
        self.Setting__c = '12345678901234567890'
        self.Membership_Level__c = ''
        self.Exclude_Account_from_AASHE_Website__c = 0
        self.is_defunct__c = False
        self.is_aashe_member__c = False
        self.Type = ''
        self.Record_Type_Name__c = ''
        self.Member_Type__c = 'campus'
        self.PCCSignatory__c = False
        self.Is_STARS_Participant__c = False
        self.STARS_Pilot_Participant__c = None
        self.Contacts = [{'Email_Address__c': 'jim@jonestown.gy'}]


class OrganizationTestCase(TestCase):

    def setUp(self):
        self.country_code = CountryCode.objects.create(
            country_name='Joe', iso_country_code='__')
        self.matching_org = Organization.objects.create(
            account_num=500,
            salesforce_id=2000,
            exclude_from_website=False)
        self.matching_account = MockSalesforceAccount(
            Account_Number__c=self.matching_org.account_num,
            Id=self.matching_org.salesforce_id,
            BillingCountry=self.country_code.country_name)
        self.not_matching_account = MockSalesforceAccount(
            Account_Number__c=1000,
            Id=1250,
            BillingCountry=self.country_code.country_name)

    def test_get_organization_for_account(self):
        """Does get_organization_for_account work?
        """
        match = Organization.get_organization_for_account(
            self.matching_account)
        self.assertEquals(self.matching_org.account_num,
                          match.account_num)

    def test_get_organization_for_account_no_match(self):
        """Is get_organization_for_account graceful when there's no match?
        """
        match = Organization.get_organization_for_account(
            self.not_matching_account)
        self.assertEquals(None, match)

    def test_get_organization_for_account_id(self):
        """Does get_organization_for_account_id work?
        """
        match = Organization.get_organization_for_account_id(
            self.matching_account.Id)
        self.assertEquals(self.matching_org.account_num,
                          match.account_num)

    def test_get_organization_for_account_id_no_match(self):
        """Is get_organization_for_account_id graceful when there's no match?
        """
        match = Organization.get_organization_for_account_id(
            self.not_matching_account.Id)
        self.assertEquals(None, match)

    def test_upsert_for_account_insert(self):
        """Does upsert_for_account work when it needs to insert a record?
        """
        match = Organization.upsert_for_account(self.not_matching_account)
        self.assertEquals(self.not_matching_account.Account_Number__c,
                          str(match.account_num))

    def test_upsert_for_account_update(self):
        """Does upsert_for_account work when it needs to update a record?
        """
        new_account_number = self.matching_account.Account_Number__c + '1'
        self.matching_account.Account_Number__c = new_account_number
        match = Organization.upsert_for_account(self.matching_account)
        self.assertEquals(new_account_number,
                          str(match.account_num))
