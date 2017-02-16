import logging

from models import Organization

from membersuite_api_client.client import ConciergeClient
from membersuite_api_client.organizations.services import OrganizationService
from django.conf import settings


logger = logging.getLogger(__name__)


def upsert_organizations_for_accounts(accounts):
    """Upserts Organizations for Salesforce Accounts `accounts`."""
    if accounts:
        client = ConciergeClient(access_key=settings.MS_ACCESS_KEY,
                                 secret_key=settings.MS_SECRET_KEY,
                                 association_id=settings.MS_ASSOCIATION_ID)
        service = OrganizationService(client)
        for account in accounts:
            logger.debug('upserting organization for account: "{account}"'.
                         format(account=account))
            Organization.upsert_for_account(account=account)
