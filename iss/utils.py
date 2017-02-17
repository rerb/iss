import logging

from models import Organization, OrganizationType
from .membersuite import MemberSuiteSession


logger = logging.getLogger(__name__)

ms_session = MemberSuiteSession()


def upsert_org_types():
    """Upserts all OrganizationTypes
    """
    org_types = ms_session.org_service.get_org_types()
    for org_type in org_types:
        OrganizationType.upsert_org_type(org_type)

def upsert_organizations(since, get_all):
    """Upserts Organizations for MemberSuite objects.
    """
    orgs = ms_session.org_service.get_orgs(get_all=get_all, since_when=since)
    if orgs:
        for org in orgs:
            logger.debug('upserting organization for org: "{org}"'.
                         format(org=org.account_num))
            Organization.upsert_organization(org=org)

def upsert_membership_products():
    """Upserts all MembershipProducts
    """
    products = ms_session.mem_service.get_all_memberships()

def upsert_memberships(since, get_all):
    """Upserts Memberships for MemberSuite objects.
    """
