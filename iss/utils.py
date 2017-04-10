import logging

from models import Organization


logger = logging.getLogger(__name__)


def upsert_organizations_for_accounts(accounts):
    """Upserts Organizations for Salesforce Accounts `accounts`."""
    for account in accounts:
        logger.debug('upserting organization for account: "{account}"'.format(
            account=account.Id))
        Organization.upsert_for_account(account=account)
