#!/usr/bin/env python
"""Upserts Organization records with data from Salesforce Accounts.
"""
import argparse
import logging
import os
import time

import salesforce
from ..utils import upsert_organizations_for_accounts


logger = logging.getLogger(os.path.basename(__file__))

parser = argparse.ArgumentParser()
parser.add_argument(
    '-m', '--modified-within',
    help='upsert organizations for accounts modified within n-days',
    type=int,
    metavar='n-days',
    default=7
)


def upsert_organizations_for_recently_modified_accounts(since=7):
    """Upsert organizations for SF Accounts modified in last `since` days."""
    logger.info('upserting orgs for accounts modified in last {since} days'.
                format(since=since))
    recently_modified_accounts = (
        salesforce.Account.get_recently_modified_accounts(since=since))
    upsert_organizations_for_accounts(recently_modified_accounts)


if __name__ == '__main__':
    logger.info('started')
    try:
        upsert_organizations_for_recently_modified_accounts(
            since=parser.parse_args().modified_within)
    except Exception:
        logger.error(('Error running '
                      'upsert_organizations_for_recently_modified_accounts'),
                     exc_info=True)
        time.sleep(1)  # time for Sentry logger thread to die
    logger.info('finished')
