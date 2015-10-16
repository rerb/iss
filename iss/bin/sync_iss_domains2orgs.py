#!/usr/bin/env python
"""Syncs iss.db Domains2Orgs with Salesforce DomainToOrg__c.
"""
import argparse
import logging
import os
import time

import iss
import salesforce


logger = logging.getLogger(os.path.basename(__file__))

parser = argparse.ArgumentParser()
parser.add_argument(
    '-m', '--modified-within',
    help='sync DomainToOrgs modified within n-days',
    type=int,
    metavar='n-days',
    default=7
)


def sync_domains2orgs():
    """Syncs Domains2Orgs with Salesforce DomainToOrg__c.
    """
    logger.info('syncing Domains2Orgs')

    all_salesforce_domains_to_orgs = (
        salesforce.DomainToOrg.get_domain_to_orgs_modified_since(
            days_ago=10000))  # 10000 days is a long time

    matches = 0
    inserts = 0

    session = iss.Session()

    # For each Salesforce DomainToOrg__c, either match it to an
    # existing ISS Domains2Orgs or create a new ISS Domains2Orgs:
    for salesforce_domains_to_orgs in all_salesforce_domains_to_orgs:
        match = iss.DomainToOrg.get_match(salesforce_domains_to_orgs,
                                          session)
        if match:
            matches += 1
        if not match:
            inserts += 1
            iss.DomainToOrg.insert(salesforce_domains_to_orgs,
                                   session)

    logger.info('{matches} Domains2Orgs matched, {inserts} inserted'.format(
        matches=matches, inserts=inserts))


if __name__ == '__main__':
    logger.info('started')
    try:
        sync_domains2orgs()
    except Exception:
        logger.error('Error running sync_domains2orgs', exc_info=True)
        time.sleep(1)  # time for Sentry logger thread to die
    logger.info('finished')
