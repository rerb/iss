import logging

from models import Organization

from membersuite_api_client.client import ConciergeClient


logger = logging.getLogger(__name__)


def upsert_organizations_for_accounts(accounts):
    """Upserts Organizations for Salesforce Accounts `accounts`."""
    if accounts:
        for account in accounts:
            formatted_account = ConciergeClient().convert_ms_object(account)
            logger.debug('upserting organization for account: "{account}"'.
                         format(account=account.Id))
            Organization.upsert_for_account(account=account)
