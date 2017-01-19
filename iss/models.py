import logging

from django.db import models


logger = logging.getLogger(__name__)


class CountryCode(models.Model):

    country_name = models.CharField(max_length=255, unique=True)
    iso_country_code = models.CharField(max_length=2, unique=True)

    @classmethod
    def get_iso_country_code(cls, country_name):
        """Returns ISO 2-digit country code for `country_name`.
        Returns empty string if `country_name` doesn't match any
        CountryCodes.
        """
        try:
            country_code = CountryCode.objects.get(country_name=country_name)
        except CountryCode.DoesNotExist:
            return ''
        return country_code.iso_country_code


class Organization(models.Model):
    account_num = models.TextField(primary_key=True)
    membersuite_id = models.IntegerField(blank=True)
    org_name = models.TextField(blank=True)
    picklist_name = models.CharField(max_length=255, blank=True)
    exclude_from_website = models.IntegerField()
    is_defunct = models.IntegerField(null=True, blank=True)
    is_member = models.IntegerField(null=True, blank=True)
    member_type = models.CharField(max_length=255, blank=True)
    business_member_level = models.CharField(max_length=255, blank=True)
    sector = models.TextField(blank=True)
    org_type = models.TextField(blank=True)
    carnegie_class = models.TextField(max_length=255, blank=True)
    class_profile = models.TextField(blank=True)
    setting = models.CharField(max_length=33, blank=True)
    longitude = models.TextField(blank=True)
    latitude = models.TextField(blank=True)
    street1 = models.TextField(blank=True)
    street2 = models.TextField(blank=True)
    city = models.TextField(blank=True)
    state = models.TextField(blank=True)
    postal_code = models.CharField(max_length=255, blank=True)
    country = models.TextField(blank=True)
    country_iso = models.CharField(max_length=3, blank=True)
    website = models.TextField(blank=True)
    sustainability_website = models.TextField(blank=True)
    enrollment_fte = models.IntegerField(null=True, blank=True)
    stars_participant_status = models.CharField(max_length=255, blank=True)
    pilot_participant = models.IntegerField(null=True, blank=True)
    is_signatory = models.IntegerField(null=True, blank=True)
    primary_email = models.CharField(max_length=256, blank=True)

    def __unicode__(self):
        return '%s (%s)' % (self.org_name, self.state)

    def __repr__(self):
        return (
            "<Organization(account_num={acct_num}, "
            "salesforce_id='{membersuite_id}')>".format(
                acct_num=self.account_num,
                membersuite_id=self.membersuite_id))

    @classmethod
    def get_attributes_for_account(cls, account):
        """Returns a dictionary of Organization attributes
        from the list of dictionaries in the Membersuite Object
        """
        logger.debug('getting attributes for account {account}'.
                     format(account=account["LocalID"]))
        account_dict = {}
        for item in account:
            account_dict[item["Key"]] = item["Value"]
        return account_dict

    @classmethod
    def get_organization_for_account(cls, account):
        """Returns the Organization that matches the given `account`.
        Returns None if no matching account is found.
        """
        logger.debug('getting organization for Org {membersuite_id}'.
                     format(membersuite_id=account["LocalID"]))
        try:
            match = Organization.objects.get(
                membersuite_id=account["LocalID"])
        except Organization.DoesNotExist:
            return None
        return match


    @classmethod
    def upsert_for_account(cls, account):
        """Upsert a matching Organization for Salesforce Account `account`.

        Returns the Organization upserted.
        """
        logger.debug('upserting account {account} into organization'.format(
            account=account["ID"]))

        matching_organization = cls.get_organization_for_account(
            account=account)
        if not matching_organization:
            matching_organization = Organization(
                account_num=account["ID"])
            logger.debug('added organization for account with Id={Id}'.format(
                Id=account.Id))
        matching_organization.update_from_account(account=account)
        return matching_organization

    def update_from_account(self, account):
        """Update this Organization from Salesforce Account `account`.
        """
        logger.debug('updating organization {account_num} '
                     'from account {membersuite_id}'.format(
                         account_num=self.account_num,
                         membersuite_id=account["LocalID"]))

        self.account_num = int(account["ID"])
        self.membersuite_id = account["LocalID"]
        self.org_name = account["Name"]
        self.picklist_name = account["SortName"]

        address = account["Addresses"]["MemberSuiteObject"]["Fields"]\
            ["KeyValueOfstringanyType"]["1"]["Value"]
        self.street1 = address["Line1"]
        self.street2 = address["Line2"]
        self.city = address["City"]
        self.state = address["State"]
        self.country = address["Country"]
        self.postal_code = address["PostalCode"]
        self.country_iso = CountryCode.get_iso_country_code(
            address["Country"])

        self.website = account["Website"]

        # self.carnegie_class = account.Carnegie_Classification__c
        # self.class_profile = (
        #     account.Carnegie_2005_Enrollment_Profile_Text__c)

        # self.enrollment_fte = account.FTE_Enrollment_All_Degrees__c
        # self.latitude = account.Latitude__c
        # self.longitude = account.Longitude__c
        # self.setting = account.Setting__c[:11]

        # self.business_member_level = account.Membership_Level__c
        # self.exclude_from_website = (
        #     account.Exclude_Account_from_AASHE_Website__c)
        self.is_defunct = (
            True if STATUSES[account["Status"]] == 'Defunct'
            else False)
        # self.is_member = account.is_aashe_member__c
        self.org_type = ORG_TYPES[account["Type"]]
        # self.sector = account.Record_Type_Name__c,
        # self.member_type = account.Member_Type__c
        # self.is_signatory = account.PCCSignatory__c
        self.stars_participant_status = (
            'STARS participant'
            if account["STARSCharterParticipant__c"]
            else '')
        # self.pilot_participant = account.STARS_Pilot_Participant__c

        self.primary_email = account['EmailAddress']

        self.save()

        logger.debug('updated organization {name} ({id})'.format(
            name=self.org_name,
            id=self.account_num))


ORG_TYPES = {
    '6faf90e4-000b-c138-b60b-0b3c5398577c': 'Business',
    '6faf90e4-000b-c491-b60c-0b3c5398577c': 'Four Year Institution',
    '6faf90e4-000b-c9ba-b60e-0b3c5398577c': 'Government Agency',
    '6faf90e4-000b-cbca-b60f-0b3c5398577c': 'Graduate Institution',
    '6faf90e4-000b-cbf6-b60d-0b3c5398577c': 'K-12 School',
    '6faf90e4-000b-cbc0-b60b-0b3c5398577c': 'Nonprofit/NGO',
    '6faf90e4-000b-cdda-b612-0b3c5398577c': 'Other',
    '6faf90e4-000b-c993-b611-0b3c5398577c': 'System Office',
    '6faf90e4-000b-c52e-b610-0b3c5398577c': 'Two Year Institution',
}

STATUSES = {
    '6faf90e4-01f3-c54c-f01a-0b3bc87640ab': 'Active',
    '6faf90e4-01f3-c0f1-4593-0b3c3ca7ff6c': 'Deceased',
    '6faf90e4-01f3-c7ad-174c-0b3c52b7f497': 'Defunct',
    '6faf90e4-01f3-cd50-ffed-0b3c3ca7f4fd': 'Retired',
}