from django.core.management.base import BaseCommand
from django.core.serializers import serialize

from optparse import make_option
import re

from .upsert_iss_organizations import (
    upsert_organizations_for_recently_modified_accounts)


class Command(BaseCommand):
    args = '<timeframe>'
    help = ('Upserts orgs from Membersuite')
    option_list = BaseCommand.option_list + (
        make_option(
            '-m',
            type=int,
            dest='m',
            default=None,
            help='upsert organizations for accounts modified within n-days'),
        make_option(
            '-i',
            dest='i',
            action='store_true',
            help='force AASHE exclude_from_website to be False'),
    )

    def handle(self, *args, **options):
        upsert_organizations_for_recently_modified_accounts(
            since=options['m'],
            include_aashe_in_website=options['i'],
        )
