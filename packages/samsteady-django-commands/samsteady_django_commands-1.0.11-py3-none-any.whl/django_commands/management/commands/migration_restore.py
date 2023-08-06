import io
from contextlib import redirect_stdout

from django.core.exceptions import ObjectDoesNotExist
from django.core.management import call_command
from django.core.management.base import BaseCommand

from django_commands.models import MigrationCheckpoint


class Command(BaseCommand):
    help = "Restores migration to checkpoint"

    def add_arguments(self, parser):
        parser.add_argument('name', type=str)

    def handle(self, *args, **options):
        name = options['name']
        try:
            found_migration_checkpoint = MigrationCheckpoint.objects.get(name=name)
            for app, migration in found_migration_checkpoint.migrations.items():
                with io.StringIO() as buf, redirect_stdout(buf):
                    call_command('migrate', app, migration, '--no-input')
                    output = buf.getvalue()
                    print(output)
                print(app, ' ', migration)
        except ObjectDoesNotExist:
            raise Exception(f'No migration found with name {name}')

