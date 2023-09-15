from django.core.management.base import BaseCommand
from django.core.serializers import serialize

from optparse import make_option
import re

from .upsert_iss_memberships import upsert_memberships_recently_modified


class Command(BaseCommand):
    args = '<timeframe>'
    help = ('Upsert Memberships modified in last `since` days')
    # option_list = BaseCommand.option_list + (
    #     make_option(
    #         '--all',
    #         dest='a',
    #         default=True,
    #         help='upsert all memberships'),
    #     make_option(
    #         '-m',
    #         type=int,
    #         dest='m',
    #         default='7',
    #         help='upsert memberships modified within n-days'),
    # )

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            dest='a',
            default=True,
            help='upsert all memberships')

        parser.add_argument(
            '-m',
            type=int,
            dest='m',
            default='7',
            help='upsert memberships modified within n-days')

    def handle(self, *args, **options):
        upsert_memberships_recently_modified(
            since=options['m'],
            get_all=options['a'],
        )
