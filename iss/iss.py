"""
Parts for the ISS end of the ISS/Salesforce sync.
"""
import logging

from sqlalchemy import Column, Date, DateTime, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import settings


logger = logging.getLogger(__name__)

engine = create_engine(settings.ISS_URL)
# engine is core interfact to db;
# engine connects to db (lazily)

Session = sessionmaker(bind=engine)
# orm's handle to database

Base = declarative_base()
# maintains catalog of classes and tables


class AthleticConference(Base):
    __tablename__ = 'athletic_conferences'

    aashe_id = Column(Integer)
    sf__id = Column(String, primary_key=True)
    name = Column(String)

    @classmethod
    def get_athletic_conference_name(cls, salesforce_id, session=None):
        """Returns name of AthleticConference with sf__id == `salesforce_id`.
        Returns None if `salesforce_id` doesn't match any AthleticConference.
        """
        session = session or Session()
        matching_athletic_conference = (session.query(cls).
                                        autoflush(False).
                                        filter_by(sf__id=salesforce_id).
                                        first())
        if matching_athletic_conference:
            return matching_athletic_conference.name


class CountryCode(Base):
    __tablename__ = 'iso_country_codes'

    id = Column(Integer, primary_key=True)
    country_name = Column(String)
    iso_2_digit = Column(String)
    iso_3_digit = Column(String)

    @classmethod
    def get_iso_country_code(cls, country_name, session=None):
        """Returns ISO 2-digit country code for `country_name`.
        Returns None if `country_name` doesn't match any CountryCodes.
        """
        session = session or Session()
        matching_country_code = (session.query(cls).
                                 autoflush(False).
                                 filter_by(country_name=country_name).
                                 first())
        if matching_country_code:
            return matching_country_code.iso_2_digit


class Domain(Base):
    __tablename__ = 'domains'

    domain_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    account_count = Column(Integer)

    def __repr__(self):
        return (
            "<Domain(domain_id={domain_id}, name='{name}')>".format(
                domain_id=self.domain_id, name=self.name))

    @classmethod
    def get_match(cls, salesforce_domain, session=None):
        """Returns the Domain that matches the given `salesforce_domain`.
        Returns None if no match is found.
        """
        session = session or Session()
        logger.debug('getting match for domain {salesforce_domain_name}'.
                     format(salesforce_domain_name=salesforce_domain.Name))
        match = (session.query(cls).
                 filter_by(domain_id=salesforce_domain.Domain_Id__c).
                 first())
        return match

    @classmethod
    def upsert(cls, salesforce_domain, session=None):
        """Upsert a Domain for `salesforce_domain`.
        """
        session = session or Session()
        logger.debug('upserting Salesforce Domain__c '
                     '"{salesforce_domain_name}" into Domain'.format(
                         salesforce_domain_name=salesforce_domain.Name))
        match = cls.get_match(salesforce_domain=salesforce_domain,
                              session=session)
        if not match:
            match = Domain()
            session.add(match)
            logger.debug('added Domain for Salesforce Domain__c '
                         '"{salesforce_domain_name}"'.format(
                             salesforce_domain_name=salesforce_domain.Name))
        match.update(salesforce_domain=salesforce_domain,
                     session=session)
        try:
            session.commit()
        except Exception:
            logger.error('Error during session.commit()', exc_info=True)

    def update(self, salesforce_domain, session=None):
        """Update this Domain from Salesforce Domain__c `salesforce_domain`.
        """
        session = session or Session()
        logger.debug('updating Domain {domain_id} from '
                     'Salesforce Domain__c "{salesforce_domain_name}"'.format(
                         domain_id=self.domain_id,
                         salesforce_domain_name=salesforce_domain.Name))

        self.domain_id = salesforce_domain.Domain_Id__c
        self.name = salesforce_domain.Name
        self.account_count = int(salesforce_domain.account_count__c)

        logger.debug('updated Domain "{name}" ({id})'.format(
            name=self.name,
            id=self.domain_id))


class DomainToOrg(Base):
    __tablename__ = 'domains2orgs'

    domain_id = Column(Integer, primary_key=True)
    org_id = Column(Integer, primary_key=True)

    def __repr__(self):
        return (
            "<DomainToOrg(org_id={org_id}, domain_id='{domain_id}')>".format(
                org_id=self.org_id, domain_id=self.domain_id))

    @classmethod
    def get_match(cls, salesforce_domain_to_org, session=None):
        """Returns the DomainToOrg that matches `salesforce_domain_to_org`.
        Returns None if no match is found.
        """
        session = session or Session()
        logger.debug('getting match for DomainToOrg with Domain Id '
                     '{domain_id} and Account Id {account_id}'.format(
                         domain_id=salesforce_domain_to_org.Domain__c,
                         account_id=salesforce_domain_to_org.Account__c))
        aashe_domain_id = salesforce_domain_to_org.Domain__r.Domain_Id__c
        aashe_org_id = salesforce_domain_to_org.Account__r.Account_Number__c
        match = (session.query(cls).
                 filter_by(domain_id=aashe_domain_id).
                 filter_by(org_id=aashe_org_id).
                 first())
        return match

    @classmethod
    def insert(cls, salesforce_domain_to_org, session=None):
        """Insert a DomainToOrg with given `domain_id` and `org_id`.
        """
        session = session or Session()
        logger.debug('inserting DomainToOrg with '
                     'Domain Id {domain_id} and Org Id {account_id}'.
                     format(domain_id=salesforce_domain_to_org.Domain__c,
                            account_id=salesforce_domain_to_org.Account__c))
        aashe_domain_id = salesforce_domain_to_org.Domain__r.Domain_Id__c
        aashe_org_id = salesforce_domain_to_org.Account__r.Account_Number__c
        domain_to_org = cls(domain_id=aashe_domain_id,
                            org_id=aashe_org_id)
        session.add(domain_to_org)
        session.commit()


class Organization(Base):
    __tablename__ = 'organizations'

    id__aashe = Column(Integer, primary_key=True)
    id__sf = Column(String)
    last_modified = Column(DateTime)
    acct__name = Column(String)
    acct__picklist_name = Column(String)
    acct__street = Column(String)
    acct__city = Column(String)
    acct__state = Column(String)
    acct__postal = Column(String)
    acct__country = Column(String)
    acct__country_iso = Column(String)
    acct__website = Column(String)
    acct__sustainability_website = Column(String)
    mem__exclude_from_website = Column(Integer)
    mem__is_defunct = Column(Integer)
    mem__is_member = Column(Integer)
    mem__type = Column(String)
    mem__biz_level = Column(String)
    mem__sector = Column(String)
    mem__org_type = Column(String)
    mem__join_date = Column(Date)
    ipeds__carnegie_class = Column(String)
    ipeds__class_profile = Column(String)
    ipeds__enrollment_fte = Column(Integer)
    ipeds__latitude = Column(String)
    ipeds__longitude = Column(String)
    ipeds__setting = Column(String)
    ipeds__basketball_conference = Column(String)
    ipeds__baseball_conference = Column(String)
    ipeds__football_conference = Column(String)
    ipeds__track_conference = Column(String)
    pcc__is_signatory = Column(Integer)
    stars__participant_status = Column(String)
    stars__pilot_participant = Column(Integer)

    def __repr__(self):
        return (
            "<Organization(id__aashe={id__aashe}, id__sf='{id__sf}')>".format(
                id__aashe=self.id__aashe, id__sf=self.id__sf))

    @classmethod
    def get_organization_for_account(cls, account, session=None):
        """Returns the Organization that matches the given `account`.
        Returns None if no matching account is found.
        """
        session = session or Session()
        logger.debug('getting organization for account {account}'.
                     format(account=account.Id))
        matching_account = (session.query(cls).
                            filter_by(id__aashe=account.Account_Number__c).
                            first())
        return matching_account

    @classmethod
    def get_organization_for_account_id(cls, account_id, session=None):
        """Returns the Organization with id__sf == `account_id`.
        Returns None if no match is found.
        """
        session = session or Session()
        logger.debug('getting organization for account_id {account_id}'.
                     format(account_id=account_id))
        organization = (session.query(cls).
                        filter_by(id__sf=account_id).
                        first())
        return organization

    @classmethod
    def upsert_for_account(cls, account, session=None):
        """Upsert a matching Organization for Salesforce Account `account`.
        """
        session = session or Session()

        logger.debug('upserting account {account} into organization'.format(
            account=account.Id))

        matching_organization = cls.get_organization_for_account(
            account=account,
            session=session)
        if not matching_organization:
            matching_organization = Organization()
            session.add(matching_organization)
            logger.debug('added organization for account with Id={Id}'.format(
                Id=account.Id))
        matching_organization.update_from_account(account=account,
                                                  session=session)
        session.commit()

    def update_from_account(self, account, session=None):
        """Update this Organization from Salesforce Account `account`.
        """
        session = session or Session()

        logger.debug('updating organization {org_id} '
                     'from account {account_id}'.format(
                         org_id=self.id__aashe,
                         account_id=account.Id))

        self.id__aashe = int(account.Account_Number__c)
        self.id__sf = account.Id
        self.acct__name = account.Name
        self.acct__picklist_name = account.picklist_name__c

        self.acct__street = account.BillingStreet
        self.acct__city = account.BillingCity
        self.acct__state = account.BillingState
        self.acct__country = account.BillingCountry
        self.acct__postal = account.BillingPostalCode
        self.acct__country_iso = CountryCode.get_iso_country_code(
            account.BillingCountry,
            session=session)

        self.acct__website = account.Website
        self.acct__sustainability_website = account.Sustainability_website__c

        self.ipeds__carnegie_class = account.Carnegie_Classification__c
        self.ipeds__class_profile = (
            account.Carnegie_2005_Enrollment_Profile_Text__c)
        self.ipeds__enrollment_fte = account.FTE_Enrollment_All_Degrees__c
        self.ipeds__latitude = account.Latitude__c
        self.ipeds__longitude = account.Longitude__c
        self.ipeds__setting = account.Setting__c[:11]

        self.ipeds__baseball_conference = (
            AthleticConference.get_athletic_conference_name(
                salesforce_id=account.Athletic_Conference_Baseball__c,
                session=session))
        self.ipeds__basketball_conference = (
            AthleticConference.get_athletic_conference_name(
                salesforce_id=account.Athletic_Conference_Basketball__c,
                session=session))
        self.ipeds__football_conference = (
            AthleticConference.get_athletic_conference_name(
                account.Athletic_Conference_Football__c,
                session=session))
        self.ipeds__track_conference = (
            AthleticConference.get_athletic_conference_name(
                account.Athletic_Conference_Track_Field__c,
                session=session))

        self.mem__biz_level = account.Membership_Level__c
        self.mem__exclude_from_website = (
            account.Exclude_Account_from_AASHE_Website__c)
        self.mem__is_defunct = account.is_defunct__c
        self.mem__is_member = account.is_aashe_member__c
        self.mem__join_date = account.Member_1st_Joined_on__c
        self.mem__org_type = account.Type
        self.mem__sector = account.Record_Type_Name__c,
        self.mem__type = account.Member_Type__c
        self.pcc__is_signatory = account.PCCSignatory__c
        self.stars__participant_status = ('STARS participant'
                                          if account.Is_STARS_Participant__c
                                          else '')
        self.stars__pilot_participant = account.STARS_Pilot_Participant__c

        logger.debug('updated organization {name} ({id})'.format(
            name=self.acct__name,
            id=self.id__aashe))


def upsert_organizations_for_accounts(accounts, session=None):
    """Upserts Organizations for Salesforce Accounts `accounts`."""
    session = session or Session()
    for account in accounts:
        logger.debug('upserting organization for account: "{account}"'.format(
            account=account.Id))
        Organization.upsert_for_account(account=account,
                                        session=session)
