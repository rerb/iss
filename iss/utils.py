import logging

from models import Organization

from membersuite_api_client.client import ConciergeClient
from django.conf import settings


logger = logging.getLogger(__name__)


def upsert_organizations_for_accounts(accounts):
    """Upserts Organizations for Salesforce Accounts `accounts`."""
    if accounts:
        client = ConciergeClient(access_key=settings.MS_ACCESS_KEY,
                                 secret_key=settings.MS_SECRET_KEY,
                                 association_id=settings.MS_ASSOCIATION_ID)
        for account in accounts:
            formatted_account = \
                client.convert_ms_object(
                    account["Fields"]["KeyValueOfstringanyType"])
            logger.debug('upserting organization for account: "{account}"'.
                         format(account=account))
            Organization.upsert_for_account(account=formatted_account)
