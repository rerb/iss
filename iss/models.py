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


class Domain(models.Model):

    domain_id = models.IntegerField(primary_key=True)
    # max_length below is for old MySQL (like the version STARS is
    # deployed with), which can't guarantee the uniqueness of a
    # variable length text blob.
    name = models.TextField(max_length=255, unique=True)
    account_count = models.IntegerField(default=0)

    def __repr__(self):
        return (
            "<Domain(domain_id={domain_id}, name='{name}')>".format(
                domain_id=self.domain_id, name=self.name))

    @classmethod
    def get_match(cls, salesforce_domain):
        """Returns the Domain that matches the given `salesforce_domain`.
        Returns None if no match is found.
        """
        logger.debug('getting match for domain {salesforce_domain_name}'.
                     format(salesforce_domain_name=salesforce_domain.Name))
        try:
            match = Domain.objects.get(
                domain_id=salesforce_domain.Domain_Id__c)
        except Domain.DoesNotExist:
            return None
        return match

    @classmethod
    def upsert(cls, salesforce_domain):
        """Upsert a Domain for `salesforce_domain`.

        Returns the Domain upserted.
        """
        logger.debug('upserting Salesforce Domain__c '
                     '"{salesforce_domain_name}" into Domain'.format(
                         salesforce_domain_name=salesforce_domain.Name))
        match = cls.get_match(salesforce_domain=salesforce_domain)
        if not match:
            match = Domain()
            logger.debug('added Domain for Salesforce Domain__c '
                         '"{salesforce_domain_name}"'.format(
                             salesforce_domain_name=salesforce_domain.Name))
        match.update(salesforce_domain=salesforce_domain)
        return match

    def update(self, salesforce_domain):
        """Update this Domain from Salesforce Domain__c `salesforce_domain`.
        """
        logger.debug('updating Domain {domain_id} from '
                     'Salesforce Domain__c "{salesforce_domain_name}"'.format(
                         domain_id=self.domain_id,
                         salesforce_domain_name=salesforce_domain.Name))

        self.domain_id = salesforce_domain.Domain_Id__c
        self.name = salesforce_domain.Name
        self.account_count = int(salesforce_domain.account_count__c)
        self.save()

        logger.debug('updated Domain "{name}" ({id})'.format(
            name=self.name,
            id=self.domain_id))


class DomainToOrg(models.Model):

    domain_id = models.IntegerField()
    org_id = models.IntegerField()

    def __repr__(self):
        return (
            "<DomainToOrg(org_id={org_id}, domain_id='{domain_id}')>".format(
                org_id=self.org_id, domain_id=self.domain_id))

    @classmethod
    def get_match(cls, salesforce_domain_to_org):
        """Returns the DomainToOrg that matches `salesforce_domain_to_org`.
        Returns None if no match is found.
        """
        logger.debug('getting match for DomainToOrg with Domain Id '
                     '{domain_id} and Account Id {account_id}'.format(
                         domain_id=salesforce_domain_to_org.Domain__c,
                         account_id=salesforce_domain_to_org.Account__c))
        aashe_domain_id = salesforce_domain_to_org.Domain__r.Domain_Id__c
        aashe_org_id = salesforce_domain_to_org.Account__r.Account_Number__c
        try:
            match = DomainToOrg.objects.get(domain_id=aashe_domain_id,
                                            org_id=aashe_org_id)
        except DomainToOrg.DoesNotExist:
            return None
        return match

    @classmethod
    def insert(cls, salesforce_domain_to_org):
        """Insert a DomainToOrg with given `domain_id` and `org_id`.

        Returns the DomainToOrg inserted.
        """
        logger.debug('inserting DomainToOrg with '
                     'Domain Id {domain_id} and Org Id {account_id}'.
                     format(domain_id=salesforce_domain_to_org.Domain__c,
                            account_id=salesforce_domain_to_org.Account__c))
        aashe_domain_id = salesforce_domain_to_org.Domain__r.Domain_Id__c
        aashe_org_id = salesforce_domain_to_org.Account__r.Account_Number__c
        new_domain_to_org = DomainToOrg.objects.create(
            domain_id=aashe_domain_id,
            org_id=aashe_org_id)
        return new_domain_to_org


class Organization(models.Model):
    account_num = models.IntegerField(primary_key=True)
    salesforce_id = models.TextField(blank=True)
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
    street = models.TextField(blank=True)
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
            "salesforce_id='{salesforce_id}')>".format(
                acct_num=self.account_num,
                salesforce_id=self.salesforce_id))

    @classmethod
    def get_organization_for_account(cls, account):
        """Returns the Organization that matches the given `account`.
        Returns None if no matching account is found.
        """
        logger.debug('getting organization for account {account}'.
                     format(account=account.Id))
        try:
            match = Organization.objects.get(
                account_num=account.Account_Number__c)
        except Organization.DoesNotExist:
            return None
        return match

    @classmethod
    def get_organization_for_account_id(cls, account_id):
        """Returns the Organization with salesforce_id == `account_id`.
        Returns None if no match is found.
        """
        logger.debug('getting organization for account_id {account_id}'.
                     format(account_id=account_id))
        try:
            match = Organization.objects.get(salesforce_id=account_id)
        except Organization.DoesNotExist:
            return None
        return match

    @classmethod
    def upsert_for_account(cls, account):
        """Upsert a matching Organization for Salesforce Account `account`.

        Returns the Organization upserted.
        """
        logger.debug('upserting account {account} into organization'.format(
            account=account.Id))

        matching_organization = cls.get_organization_for_account(
            account=account)
        if not matching_organization:
            matching_organization = Organization(
                account_num=int(account.Account_Number__c))
            logger.debug('added organization for account with Id={Id}'.format(
                Id=account.Id))
        matching_organization.update_from_account(account=account)
        return matching_organization

    def update_from_account(self, account):
        """Update this Organization from Salesforce Account `account`.
        """
        logger.debug('updating organization {org_id} '
                     'from account {account_id}'.format(
                         org_id=self.account_num,
                         account_id=account.Id))

        self.account_num = int(account.Account_Number__c)
        self.salesforce_id = account.Id
        self.org_name = account.Name
        self.picklist_name = account.picklist_name__c

        self.street = account.BillingStreet
        self.city = account.BillingCity
        self.state = account.BillingState
        self.country = account.BillingCountry
        self.postal = account.BillingPostalCode
        self.country_iso = CountryCode.get_iso_country_code(
            account.BillingCountry)

        self.website = account.Website
        self.sustainability_website = account.Sustainability_website__c

        self.carnegie_class = account.Carnegie_Classification__c
        self.class_profile = (
            account.Carnegie_2005_Enrollment_Profile_Text__c)
        self.enrollment_fte = account.FTE_Enrollment_All_Degrees__c
        self.latitude = account.Latitude__c
        self.longitude = account.Longitude__c
        self.setting = account.Setting__c[:11]

        self.business_member_level = account.Membership_Level__c
        self.exclude_from_website = (
            account.Exclude_Account_from_AASHE_Website__c)
        self.is_defunct = account.is_defunct__c
        self.is_member = account.is_aashe_member__c
        self.org_type = account.Type
        self.sector = account.Record_Type_Name__c,
        self.member_type = account.Member_Type__c
        self.is_signatory = account.PCCSignatory__c
        self.stars_participant_status = (
            'STARS participant'
            if account.Is_STARS_Participant__c
            else '')
        self.pilot_participant = account.STARS_Pilot_Participant__c

        if account.Contacts:
            self.primary_email = account.Contacts[0]['Email_Address__c']

        self.save()

        logger.debug('updated organization {name} ({id})'.format(
            name=self.org_name,
            id=self.account_num))
