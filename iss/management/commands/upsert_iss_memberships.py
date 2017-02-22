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
            '-m', '--modified-within',
            type=int,
            dest='m',
            metavar='n-days',
            default=7,
            help='upsert memberships modified within n-days'
        )

    def handle(self, *args, **options):
        upsert_memberships_recently_modified(
            since=options['m'],
        )


def upsert_memberships_recently_modified(since=7, get_all=False):
    """Upsert Memberships modified in last `since` days.

    First syncs MembershipProduct objects, then Memberships.

    Then loops through memberships and makes sure ForeignKey is properly set
    on the owner organization.
    """
    logger.info('upserting MembershipProducts')
    iss.utils.upsert_membership_products()

    logger.info('upserting memberships modified in last {since} days'.
                format(since=since))
    iss.utils.upsert_memberships(since)

    logger.info('upserting membership owners')
    iss.utils.upsert_membership_ownerships()
