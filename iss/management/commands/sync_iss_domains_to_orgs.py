#!/usr/bin/env python
"""Syncs DomainToOrg with Salesforce DomainToOrg__c.
"""
import logging
import os

from django.core.management.base import BaseCommand

import iss.models
import iss.salesforce


logger = logging.getLogger(os.path.basename(__file__))


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-m', '--modified-within',
                            type=int,
                            metavar='n-days',
                            default=7,
                            help='sync DomainToOrgs modified within n-days')

    def handle(self, *args, **options):
        sync_domain_to_org()


def sync_domain_to_org():
    """Syncs DomainToOrg with Salesforce DomainToOrg__c.
    """
    logger.info('syncing DomainsToOrg')

    all_salesforce_domains_to_orgs = (
        iss.salesforce.DomainToOrg.get_domain_to_orgs_modified_since(
            days_ago=10000))  # 10000 days is a long time

    matches = 0
    inserts = 0

    # For each Salesforce DomainToOrg__c, either match it to an
    # existing DomainsToOrg or create a new DomainsToOrg:
    for salesforce_domains_to_orgs in all_salesforce_domains_to_orgs:
        match = iss.models.DomainToOrg.get_match(salesforce_domains_to_orgs)
        if match:
            matches += 1
        if not match:
            inserts += 1
            iss.models.DomainToOrg.insert(salesforce_domains_to_orgs)

    logger.info('{matches} DomainsToOrg matched, {inserts} inserted'.format(
        matches=matches, inserts=inserts))
