#!/usr/bin/env python
"""Deletes Organization records that don't match any Salesforce Account.
"""
import logging
import os

from django.core.management.base import BaseCommand

import iss.models
import iss.salesforce


logger = logging.getLogger(os.path.basename(__file__))


class Command(BaseCommand):

    def handle(self, *args, **options):
        delete_organizations_for_deleted_accounts()


def delete_organizations_for_deleted_accounts():
    """Delete organizations for all deleted SF Accounts.
    """
    logger.debug('deleting orgs for all deleted accounts')
    all_account_ids = iss.salesforce.Account.get_ids_for_all_accounts()
    logger.debug('got {len} Account IDs'.format(len=len(all_account_ids)))
    logger.debug('{count} total Organizations'.format(
        count=iss.models.Organization.objects.count()))
    organizations_to_delete = iss.models.Organization.objects.exclude(
        salesforce_id__in=all_account_ids)
    logger.debug('{count} Organizations to delete'.format(
        count=organizations_to_delete.count()))
    organizations_to_delete.delete()
