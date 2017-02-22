import logging

from models import Organization, OrganizationType, \
    Membership, MembershipProduct
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
    products = ms_session.mem_service.get_all_membership_products()
    for product in products:
        logger.debug('upserting membership products')
        MembershipProduct.upsert_membership_product(product=product)

def upsert_memberships(since):
    """Upserts Memberships for MemberSuite objects.
    """
    memberships = ms_session.mem_service.get_all_memberships(since_when=since)
    if memberships:
        for membership in memberships:
            logger.debug('upserting membership {mem}'.format(
                mem=membership.id)
            )
            Membership.upsert_membership(membership=membership)

def upsert_membership_ownerships():
    """Upserts the owners associated with memberships
    """
    memberships = Membership.objects.all()
    for membership in memberships:
        if (membership.status != 'Expired' and
                membership.status != 'Terminated' and
                membership.status != 'Pending' and
                membership.owner):

            membership.owner.is_member = True
            membership.owner.member_type = membership.product.name
            if membership.owner.org_type.name != 'Campus':
                if "Leader" in membership.product.name:
                    membership.owner.business_member_level = \
                        "Business Leader"
                    membership.owner.save()
                if "Supporter" in membership.product.name:
                    membership.owner.business_member_level = \
                        "Business Supporter"
                    membership.owner.save()
                if "Affiliate" in membership.product.name:
                    membership.owner.business_member_level = \
                        "Business Affiliate"
                    membership.owner.save()
