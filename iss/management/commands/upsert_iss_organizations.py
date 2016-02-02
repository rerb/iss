#!/usr/bin/env python
"""Upserts Organization records with data from Salesforce Accounts.
"""
import logging
import os

from django.core.management.base import BaseCommand

import iss.models
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
        parser.add_argument(
            '-i', '--include-aashe-in-website',
            action='store_true',
            help='force AASHE exclude_from_website to be False')

    def handle(self, *args, **options):
        upsert_organizations_for_recently_modified_accounts(
            since=options['modified_within'],
            include_aashe_in_website=options['include_aashe_in_website'])


def upsert_organizations_for_recently_modified_accounts(
        since=7, include_aashe_in_website=False):
    """Upsert organizations for SF Accounts modified in last `since` days.

    When `include_aashe_in_website` is true, set the
    `exclude_from_website` flag on the Organization representing AASHE
    to False (0, actually).  (Added for the Hub project.)
    """
    logger.info('upserting orgs for accounts modified in last {since} days'.
                format(since=since))
    recently_modified_accounts = (
        iss.salesforce.Account.get_recently_modified_accounts(since=since))
    iss.utils.upsert_organizations_for_accounts(recently_modified_accounts)

    if include_aashe_in_website:
        aashe = iss.models.Organization.objects.get(org_name="AASHE")
        if aashe.exclude_from_website:
            aashe.exclude_from_website = 0
            aashe.save()
