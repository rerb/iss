#!/usr/bin/env python
"""Upserts Domains from Salesforce Domain__c.
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
                            help='upsert Domains modified within n-days')

    def handle(self, *args, **options):
        upsert_domains(options['modified_within'])


def upsert_domains(modified_since=7):
    """Upsert Domains for SF Domain__c modified in last `modified_since` days.
    """
    logger.info('upserting domains modified in last {since} days'.
                format(since=modified_since))
    modified_domains = (iss.salesforce.Domain.get_domains_modified_since(
        days_ago=modified_since))
    for domain in modified_domains:
        iss.models.Domain.upsert(domain)
