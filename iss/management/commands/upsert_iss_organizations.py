#!/usr/bin/env python
"""Upserts Organization records with data from Salesforce Accounts.
"""
import logging
import os

from django.core.management.base import BaseCommand

import iss.models
import iss.membersuite
import iss.utils


logger = logging.getLogger(os.path.basename(__file__))


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '-a', '--all',
            type=bool,
            dest='a',
            help='upsert all organizations'
        )
        parser.add_argument(
            '-m', '--modified-within',
            type=int,
            dest='m',
            metavar='n-days',
            default=7,
            help='upsert organizations for accounts modified within n-days'
        )
        parser.add_argument(
            '-i', '--include-aashe-in-website',
            dest='i',
            action='store_true',
            help='force AASHE exclude_from_website to be False'
        )

    def handle(self, *args, **options):
        upsert_organizations_for_recently_modified_accounts(
            since=options['m'],
            include_aashe_in_website=options['i'],
            get_all=options['a'],
        )


def upsert_organizations_for_recently_modified_accounts(
        since=7, include_aashe_in_website=False, get_all=False):
    """Upsert organizations for MS Accounts modified in last `since` days.

    First syncs OrganizationType objects, then Organizations.

    When `include_aashe_in_website` is true, set the
    `exclude_from_website` flag on the Organization representing AASHE
    to False (0, actually).  (Added for the Hub project.)
    """
    logger.info('upserting OrganizationTypes')
    iss.utils.upsert_org_types()

    logger.info('upserting orgs for accounts modified in last {since} days'.
                format(since=since))
    iss.utils.upsert_organizations(since, get_all)

    if include_aashe_in_website:
        aashe = iss.models.Organization.objects.get(org_name="AASHE")
        if aashe.exclude_from_website:
            aashe.exclude_from_website = 0
            aashe.save()
