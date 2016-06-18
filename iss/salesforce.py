"""
Parts for the Salesforce end of the ISS/Salesforce sync.
"""
import datetime
import logging

import beatbox
from django.conf import settings


logger = logging.getLogger(__name__)


class SalesforceSession(object):

    def __init__(self):
        self.service = beatbox.PythonClient()
        self.login()

    def login(self):
        self.service.login(settings.SALESFORCE_USERNAME,
                           settings.SALESFORCE_PASSWORD +
                           settings.SALESFORCE_SECURITY_TOKEN)
        self.service.batchSize = 2000  # max

    def query_all(self, query):
        """Returns results from submitting `query` until there are no more.
        """
        logger.debug('submitting query "{query}"'.format(query=query))
        all_results = results = self.service.query(query)
        while results['queryLocator']:
            logger.debug('querying more for "{query}"'.format(query=query))
            results = self.service.queryMore(results['queryLocator'])
            all_results += results
        return all_results

    def get_objects_modified_since(self,
                                   object_name,
                                   object_fields,
                                   days_ago):
        """Return objects modified within `days_ago` days.

        `object_name` identifies the object (e.g., 'Account')
        `object_fields` is a list of fields to return for each object
        """
        since_when = datetime.date.today() - datetime.timedelta(days_ago)
        query = ('SELECT {fields} FROM {object} '
                 'WHERE lastmodifieddate > {since}T00:00:00Z'.format(
                     fields=','.join(object_fields),
                     object=object_name,
                     since=since_when.isoformat()))
        return self.query_all(query=query)


class SalesforceObject(object):

    session = None

    def __new__(cls, salesforce_session=None, *args, **kwargs):
        cls.session = salesforce_session or SalesforceSession()
        return super(object, cls).__new__(*args, **kwargs)


class Account(SalesforceObject):

    MAPPED_ACCOUNT_FIELDS = ['Id',
                             'Name',
                             'Account_Num_int__c',
                             'Account_Number__c',
                             'Athletic_Conference_Baseball__c',
                             'Athletic_Conference_Basketball__c',
                             'Athletic_Conference_Football__c',
                             'Athletic_Conference_Track_Field__c',
                             'BillingCity',
                             'BillingCountry',
                             'BillingPostalCode',
                             'BillingState',
                             'BillingStreet',
                             'Carnegie_2005_Enrollment_Profile_Text__c',
                             'Carnegie_Classification__c',
                             'Exclude_Account_from_AASHE_Website__c',
                             'FTE_Enrollment_All_Degrees__c',
                             'Is_STARS_Participant__c',
                             'LastModifiedDate',
                             'Latitude__c',
                             'Longitude__c',
                             'Member_1st_Joined_on__c',
                             'Member_Type__c',
                             'Membership_Level__c',
                             'PCCSignatory__c',
                             'Record_Type_Name__c',
                             'STARS_Pilot_Participant__c',
                             'Setting__c',
                             'Sustainability_website__c',
                             'Type',
                             'Website',
                             'is_aashe_member__c',
                             'is_defunct__c',
                             'picklist_name__c']

    @classmethod
    def get_accounts_modified_since(cls, days_ago, session=None):
        """Return all Accounts modified within `days_ago` days."""
        cls.session = session or SalesforceSession()
        since_when = datetime.date.today() - datetime.timedelta(days_ago)
        query = ("""
        SELECT {all_fields},
        (SELECT Member_Contact_Role__c, Email_Address__c
         FROM contacts WHERE Member_Contact_Role__c = 'Primary Contact'
         LIMIT 1)
        FROM ACCOUNT
        WHERE lastmodifieddate > {since_when}T00:00:00Z""".format(
            all_fields=','.join(cls.MAPPED_ACCOUNT_FIELDS),
            since_when=since_when.isoformat()))
        return cls.session.query_all(query=query)

    @classmethod
    def get_recently_modified_accounts(cls, since=7, session=None):
        """Returns Salesforce Accounts modified within `since` days."""
        cls.session = session or SalesforceSession()
        recently_modified_accounts = (
            cls.get_accounts_modified_since(days_ago=since,
                                            session=cls.session))
        logger.info('{number} accounts modifed in past {since} days'.format(
            number=recently_modified_accounts.size, since=since))
        return recently_modified_accounts

    @classmethod
    def get_ids_for_all_accounts(cls, session=None):
        """Return IDs of all Accounts.
        """
        cls.session = session or SalesforceSession()
        query = ("SELECT Id FROM ACCOUNT")
        query_result = cls.session.query_all(query=query)
        ids = [account["Id"] for account in query_result]
        return ids


class Domain(SalesforceObject):

    @classmethod
    def get_domains_modified_since(cls, days_ago, session=None):
        """Return all Domain__c objects modified within `days_ago` days."""
        cls.session = session or SalesforceSession()
        return cls.session.get_objects_modified_since(
            object_name='Domain__c',
            object_fields=['Domain_Id__c',
                           'Name',
                           'Account_Count__c'],
            days_ago=days_ago)


class DomainToOrg(SalesforceObject):

    @classmethod
    def get_domain_to_orgs_modified_since(cls, days_ago, session=None):
        """Return the DomainToOrg__c objects modified with `days_ago` days.
        """
        cls.session = session or SalesforceSession()
        return cls.session.get_objects_modified_since(
            object_name='DomainToOrg__c',
            object_fields=['Domain__r.Domain_Id__c',
                           'Account__r.Account_Number__c',
                           'Domain__c',
                           'Account__c'],
            days_ago=days_ago)
