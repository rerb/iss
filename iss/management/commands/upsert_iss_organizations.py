#!/usr/bin/env python
"""Upserts Organization records with data from Salesforce Accounts.
"""
import logging
import os

from django.core.management.base import BaseCommand

import iss.salesforce
import iss.utils


logger = logging.getLogger(os.path.basename(__file__))


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '-m', '--modified-within',
            type=int,
            metavar='n-days',
            default=7,
            help='upsert organizations for accounts modified within n-days')

    def handle(self, *args, **options):
        upsert_organizations_for_recently_modified_accounts(
            options['modified_within'])


def upsert_organizations_for_recently_modified_accounts(since=7):
    """Upsert organizations for SF Accounts modified in last `since` days."""
    logger.info('upserting orgs for accounts modified in last {since} days'.
                format(since=since))
    recently_modified_accounts = (
        iss.salesforce.Account.get_recently_modified_accounts(since=since))
    iss.utils.upsert_organizations_for_accounts(recently_modified_accounts)
