from django.core.management.base import BaseCommand, CommandError
from accounts.tests.factories import UserFactory


class Command(BaseCommand):
    help = 'Insert dummy users and dummy snippets'

    def add_arguments(self, parser):
        parser.add_argument('account_count', nargs='?', type=int)

    def handle(self, *args, **options):
        account_count = options.get("account_count")
        if not account_count:
            account_count = 1000

        for i in range(account_count):
            UserFactory()
