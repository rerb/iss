#!/usr/bin/env python
"""Upserts Domains from Salesforce Domain__c.
"""
import argparse
import logging
import os
import time

import salesforce
from ..models import Domain


logger = logging.getLogger(os.path.basename(__file__))

parser = argparse.ArgumentParser()
parser.add_argument(
    '-m', '--modified-within',
    help='upsert domain info modified within n-days',
    type=int,
    metavar='n-days',
    default=7
)


def upsert_domains(modified_since=7):
    """Upsert Domains for SF Domain__c modified in last `modified_since` days.
    """
    logger.info('upserting domains modified in last {since} days'.
                format(since=modified_since))
    modified_domains = (salesforce.Domain.get_domains_modified_since(
        days_ago=modified_since))
    for domain in modified_domains:
        Domain.upsert(domain)


if __name__ == '__main__':
    logger.info('started')
    try:
        upsert_domains(modified_since=parser.parse_args().modified_within)
    except Exception:
        logger.error('Error running upsert_domains', exc_info=True)
        time.sleep(1)  # time for Sentry logger thread to die
    logger.info('finished')
