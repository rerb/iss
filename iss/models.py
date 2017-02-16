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
    account_num = models.CharField(primary_key=True, max_length=255)
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
    def get_organization_for_account(cls, account):
        """Returns the Organization that matches the given `account`.
        Returns None if no matching account is found.
        """
        logger.debug('getting organization for Org {membersuite_id}'.
                     format(membersuite_id=account.membersuite_id))
        try:
            match = Organization.objects.get(
                account_num=account.account_num)
        except Organization.DoesNotExist:
            return None
        return match

    @classmethod
    def upsert_for_account(cls, account):
        """Upsert a matching Organization for Salesforce Account `account`.

        Returns the Organization upserted.
        """
        logger.debug('upserting account {account} into organization'.format(
            account=account.account_num))

        matching_organization = cls.get_organization_for_account(
            account=account)
        if not matching_organization:
            matching_organization = Organization(
                account_num=account.account_num)
            logger.debug('added organization for account with Id={Id}'.format(
                Id=account.account_num))
        matching_organization.update_from_account(account=account)
        return matching_organization

    def update_from_account(self, account):
        """Update this Organization from Membersuite Organization object.
        """
        logger.debug('updating organization {membersuite_id} '
                     'from account {account_num}'.format(
                         account_num=self.account_num,
                         membersuite_id=account.membersuite_id))

        self.account_num = account.account_num
        self.membersuite_id = account.membersuite_id
        self.org_name = account.org_name
        self.picklist_name = account.picklist_name

        self.street1 = account.street1
        self.street2 = account.street2
        self.city = account.city
        self.state = account.state
        self.country = account.country
        self.postal_code = account.postal_code
        self.country_iso = CountryCode.get_iso_country_code(
            self.country)
        self.latitude = account.latitude
        self.longitude = account.longitude

        self.website = account.website

        # self.carnegie_class = account.Carnegie_Classification__c
        # self.class_profile = (
        #     account.Carnegie_2005_Enrollment_Profile_Text__c)

        # self.enrollment_fte = account.FTE_Enrollment_All_Degrees__c
        # self.setting = account.Setting__c[:11]

        # self.business_member_level = account.Membership_Level__c
        self.exclude_from_website = False
        self.is_defunct = account.is_defunct
        # self.is_member = account.is_aashe_member__c
        self.org_type = account.org_type
        # self.sector = account.Record_Type_Name__c,
        # self.member_type = account.Member_Type__c
        # self.is_signatory = account.PCCSignatory__c
        # self.stars_participant_status = ?
        # self.pilot_participant = account.STARS_Pilot_Participant__c

        self.primary_email = account.primary_email

        self.save()

        logger.debug('updated organization {name} ({id})'.format(
            name=self.org_name,
            id=self.account_num))


class OrganizationType(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    name = models.TextField()

    def __unicode__(self):
        return self.name

    @classmethod
    def upsert_org_type(cls, org_type):
        """
        Upsert an OrganizationType

        Returns the OrganizationType upserted
        """
        logger.debug('upserting org type {name} into org type'.format(
            name=org_type.name))
        matching_org_type = cls.get_org_type_for_id(org_type=org_type)
        if not matching_org_type:
            matching_org_type = OrganizationType(
                id=org_type.id,
                name=org_type.name,
            )
            logger.debug('added org type for Id={Id}'.format(
                Id=org_type.id))
        matching_org_type.update_org_type(org_type=org_type)
        return matching_org_type

    @classmethod
    def get_org_type_for_id(cls, org_type):
        """Returns the OrganizationType that matches the given ID.
        Returns None if no matching ID is found.
        """
        logger.debug('getting org type for {name}'.
                     format(name=org_type.name))
        try:
            match = OrganizationType.objects.get(id=org_type.id)
        except OrganizationType.DoesNotExist:
            return None
        return match

    def update_org_type(self, org_type):
        """Update this OrganizationType from MemberSuite object
        """
        logger.debug('updating org type {name} '
                     'from id {id}'.format(name=org_type.name, id=org_type.id))
        self.name = org_type.name
        self.save()
        logger.debug('updated org type {name} ({id})'.format(name=self.name,
                                                             id=self.id))
    

class Membership(models.Model):
    
    STATUSES = {
        '6faf90e4-01f3-c54c-f01a-0b3bc87640ab': 'Active',
        '6faf90e4-01f3-c0f1-4593-0b3c3ca7ff6c': 'Deceased',
        '6faf90e4-01f3-c7ad-174c-0b3c52b7f497': 'Defunct',
        '6faf90e4-01f3-cd50-ffed-0b3c3ca7f4fd': 'Retired',
    }

    id = models.CharField(primary_key=True, max_length=255)
    owner = models.ForeignKey(Organization)
    membership_directory_opt_out = models.BooleanField()
    receives_membership_benefits = models.BooleanField()
    current_dues_amount = models.CharField(max_length=255)
    expiration_date = models.DateField()
    type = models.CharField(max_length=255)
    product = models.ForeignKey(MembershipProduct)
    last_modified_date = models.DateField()
    status = models.CharField(choices=STATUSES, max_length=255)
    join_date = models.DateField()
    termination_date = models.DateField()
    renewal_date = models.DateField()
    
    @classmethod
    def upsert_membership(cls, membership):
        """
        Upserts a Membership from MemberSuite Membership object.
        
        Returns the Membership upserted.
        """
        logger.debug('upserting org type {name} into org type'.format(
            name=membership.name))
        matching_membership = cls.get_membership_for_id(membership=membership)
        if not matching_membership:
            matching_membership = Membership(id=membership.id)
            logger.debug('added membership for ID={id}'.format(
                id=membership.id))
        matching_membership.update_membership(membership=membership)
        return matching_membership

    @classmethod
    def get_membership_for_id(cls, membership):
        """Returns the Membership that matches the given ID.
        Returns None if no matching ID is found.
        """
        logger.debug('getting org type for {id}'.
                     format(id=membership.id))
        try:
            match = Membership.objects.get(id=membership.id)
        except OrganizationType.DoesNotExist:
            return None
        return match

    def update_membership(self, membership):
        """Update this Membership from MemberSuite Membership object
        """
        logger.debug('updating membership {id}'.format(id=membership.id))

        self.owner = Organization.objects.get(id=membership.owner)
        self.membership_directory_opt_out = \
            membership.membership_directory_opt_out
        self.receives_membership_benefits = \
            membership.receives_membership_benefits
        self.current_dues_amount = membership.current_dues_amount
        self.expiration_date = membership.expiration_date
        self.type = membership.type
        self.product = MembershipProduct.objects.get(id=membership.product)
        self.last_modified_date = membership.last_modified_date
        self.status = membership.status
        self.join_date = membership.join_date
        self.termination_date = membership.termination_date
        self.renewal_date = membership.renewal_date
        self.save()
        logger.debug('updated membership ({id})'.format(id=self.id))


class MembershipProduct(models.Model):

    id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)

    @classmethod
    def upsert_membership_product(cls, product):
        """
        Upserts a MembershipProduct from MemberSuite MembershipProduct object.

        Returns the MembershipProduct upserted.
        """
        logger.debug('upserting org type {name} into org type'.format(
            name=product.name))
        matching_product = cls.get_product_for_id(product=product)
        if not matching_product:
            matching_product = MembershipProduct(id=product.id)
            logger.debug('added membership for ID={id}'.format(
                id=product.id))
        matching_product.update_membership(product=product)
        return matching_product

    @classmethod
    def get_product_for_id(cls, product):
        """Returns the MembershipProduct that matches the given ID.
        Returns None if no matching ID is found.
        """
        logger.debug('getting org type for {id}'.
                     format(id=product.id))
        try:
            match = MembershipProduct.objects.get(id=product.id)
        except MembershipProduct.DoesNotExist:
            return None
        return match

    def update_membership_product(self, product):
        """Update this MembershipProduct from MemberSuite object
        """
        logger.debug('updating membership product {id}'.format(
            id=product.id))
        self.name = product.name
