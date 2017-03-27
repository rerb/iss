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


class Organization(models.Model):
    account_num = models.AutoField(primary_key=True)
    salesforce_id = models.TextField(blank=True, null=True)
    membersuite_account_num = models.CharField(blank=True, null=True,
                                               max_length=255)
    membersuite_id = models.IntegerField(blank=True, null=True)
    org_name = models.TextField(blank=True, null=True)
    picklist_name = models.CharField(max_length=255, blank=True, null=True)
    exclude_from_website = models.IntegerField()
    is_defunct = models.IntegerField(default=0)
    is_member = models.IntegerField(default=0)
    member_type = models.CharField(max_length=255, blank=True, null=True)
    business_member_level = models.CharField(max_length=255, blank=True,
                                             null=True)
    sector = models.TextField(blank=True, null=True)
    org_type = models.ForeignKey(OrganizationType, null=True)
    carnegie_class = models.TextField(max_length=255, blank=True, null=True)
    class_profile = models.TextField(blank=True, null=True)
    setting = models.CharField(max_length=33, blank=True, null=True)
    longitude = models.TextField(blank=True, null=True)
    latitude = models.TextField(blank=True, null=True)
    street1 = models.TextField(blank=True, null=True)
    street2 = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    postal_code = models.CharField(max_length=255, blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    country_iso = models.CharField(max_length=3, blank=True, null=True)
    website = models.TextField(blank=True, null=True)
    sustainability_website = models.TextField(blank=True, null=True)
    enrollment_fte = models.IntegerField(null=True, blank=True)
    stars_participant_status = models.CharField(max_length=255, blank=True,
                                                null=True)
    pilot_participant = models.IntegerField(null=True, blank=True)
    is_signatory = models.IntegerField(null=True, blank=True)
    primary_email = models.CharField(max_length=256, blank=True, null=True)

    def __unicode__(self):
        return '%s (%s)' % (self.org_name, self.state)

    def __repr__(self):
        return (
            "<Organization(account_num={acct_num}, "
            "membersuite_id='{membersuite_id}')>".format(
                acct_num=self.account_num,
                membersuite_id=self.membersuite_id))

    @classmethod
    def get_organization_for_id(cls, org):
        """Returns the Organization that matches the given `account`.
        Returns None if no matching account is found.
        """
        logger.debug('getting organization for Org {id}'.format(
            id=org.account_num)
        )
        try:
            match = Organization.objects.get(
                membersuite_account_num=org.account_num)
        except Organization.DoesNotExist:
            match = None

        if org.extra_data["SalesforceID__c"] and not match:
            try:
                match = Organization.objects.get(
                    salesforce_id=org.extra_data["SalesforceID__c"])
            except Organization.DoesNotExist:
                return None

        return match

    @classmethod
    def upsert_organization(cls, org):
        """Upsert a matching Organization for MemberSuite object.

        Returns the Organization upserted.
        """
        logger.debug('upserting org {id}'.format(id=org.account_num))

        matching_organization = cls.get_organization_for_id(org=org)
        if not matching_organization:
            matching_organization = Organization(
                membersuite_account_num=org.account_num)
            logger.debug('added organization for Id={Id}'.format(
                Id=org.account_num))
        matching_organization.update_organization(org=org)
        return matching_organization

    def update_organization(self, org):
        """Update this Organization from Membersuite Organization object.
        """
        logger.debug('updating organization {id} '
                     'from account {account_num}'.format(
                         account_num=self.account_num,
                         id=org.account_num))

        self.membersuite_account_num = org.account_num
        self.membersuite_id = org.membersuite_id
        self.salesforce_id = org.extra_data.get("SalesforceID__c", None)
        self.org_name = org.org_name
        self.picklist_name = org.picklist_name

        if org.address:
            self.street1 = org.street1
            self.street2 = org.street2
            self.city = org.city
            self.state = org.state
            self.country = org.country
            self.postal_code = org.postal_code
            self.country_iso = CountryCode.get_iso_country_code(
                self.country)
            self.latitude = org.latitude
            self.longitude = org.longitude

        self.website = org.website

        # self.carnegie_class = org.Carnegie_Classification__c
        # self.class_profile = (
        #     org.Carnegie_2005_Enrollment_Profile_Text__c)

        # self.enrollment_fte = org.FTE_Enrollment_All_Degrees__c
        # self.setting = org.Setting__c[:11]

        # self.business_member_level = org.Membership_Level__c
        self.exclude_from_website = False
        self.is_defunct = org.is_defunct
        # self.is_member = org.is_aashe_member__c
        self.org_type = OrganizationType.objects.get(id=org.org_type)
        # self.sector = org.Record_Type_Name__c,
        # self.member_type = org.Member_Type__c
        # self.is_signatory = org.PCCSignatory__c
        # self.stars_participant_status = ?
        # self.pilot_participant = org.STARS_Pilot_Participant__c

        self.primary_email = org.primary_email

        self.save()

        logger.debug('updated organization {name})'.format(
            name=org.org_name.encode('utf-8')))


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
        matching_product.update_membership_product(product=product)
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
        self.save()


class Membership(models.Model):

    id = models.CharField(primary_key=True, max_length=255)
    owner = models.ForeignKey(Organization, null=True)
    membership_directory_opt_out = models.BooleanField(default=False)
    receives_membership_benefits = models.BooleanField(default=True)
    current_dues_amount = models.CharField(max_length=255,
                                           blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    type = models.CharField(max_length=255)
    product = models.ForeignKey(MembershipProduct)
    last_modified_date = models.DateField()
    status = models.CharField(max_length=255)
    join_date = models.DateField(blank=True, null=True)
    termination_date = models.DateField(blank=True, null=True)
    renewal_date = models.DateField(blank=True, null=True)

    @classmethod
    def upsert_membership(cls, membership):
        """
        Upserts a Membership from MemberSuite Membership object.

        Returns the Membership upserted.
        """
        logger.debug('upserting membership {id}'.format(
            id=membership.id))
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
        logger.debug('getting membership {id}'.
                     format(id=membership.id))
        try:
            match = Membership.objects.get(id=membership.id)
        except Membership.DoesNotExist:
            return None
        return match

    def update_membership(self, membership):
        """Update this Membership from MemberSuite Membership object
        """
        logger.debug('updating membership {id}'.format(id=membership.id))
        try:
            self.owner = Organization.objects.get(
                membersuite_account_num=membership.owner)
        except Organization.DoesNotExist:
            pass
        self.membership_directory_opt_out = \
            membership.membership_directory_opt_out
        self.receives_membership_benefits = \
            membership.receives_member_benefits
        self.current_dues_amount = membership.current_dues_amount
        self.expiration_date = membership.expiration_date
        self.type = membership.type
        self.product = MembershipProduct.objects.get(id=membership.product)
        self.last_modified_date = membership.last_modified_date
        if membership.status:
            self.status = STATUSES[membership.status]
        self.join_date = membership.join_date
        self.termination_date = membership.termination_date
        self.renewal_date = membership.renewal_date
        self.save()
        logger.debug('updated membership ({id})'.format(id=self.id))


STATUSES = {
    '6faf90e4-0069-cf2c-650f-0b3c15a7d3aa': 'Expired',
    '6faf90e4-0069-cd19-6a43-0b3c15a7c287': 'New Member',
    '6faf90e4-0069-c450-a9c8-0b3c6a781755': 'Pending',
    '6faf90e4-0069-c7d5-2e88-0b3c15a7cf8a': 'Reinstated',
    '6faf90e4-0069-c2ef-6d51-0b3c15a7cb7f': 'Renewed',
    '6faf90e4-0069-cebb-b501-0b3c15a7d742': 'Terminated',
}
