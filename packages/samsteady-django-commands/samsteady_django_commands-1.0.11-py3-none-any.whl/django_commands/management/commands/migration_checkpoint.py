import io
import traceback
from contextlib import redirect_stdout
from pprint import pprint

from django.core.exceptions import ObjectDoesNotExist
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from django_commands.models import MigrationCheckpoint


class Command(BaseCommand):
    help = "Create db migrations checkpoint for future rollbacks of all apps at once"

    def add_arguments(self, parser):
        parser.add_argument('name', type=str)

    def handle(self, *args, **options):
        name = options['name']
        try:
            found = MigrationCheckpoint.objects.get(name=name)
            print(f'Found existing migration checkpoint with name {name}')
            return
        except ObjectDoesNotExist:
            pass

        try:
            with io.StringIO() as buf, redirect_stdout(buf):
                call_command("showmigrations")
                output = buf.getvalue()
            prev_line = None
            lines = output.splitlines()
            lines.append('')
            curr_app = None
            migrations = {}
            for line in lines:
                if not prev_line:
                    prev_line = line
                    continue
                if not curr_app and not prev_line.startswith(' [X]') and line.startswith(' [X]'):
                    curr_app = prev_line
                if prev_line.startswith(' [X]') and not line.startswith(' [X]'):
                    try:
                        migration = prev_line.split(' ')[2]
                        if not curr_app:
                            raise Exception("No app found...")
                        migrations[curr_app] = migration
                        curr_app = None
                    except Exception as e:
                        traceback.print_exc()
                prev_line = line

            migration_checkpoint = MigrationCheckpoint(name=name, migrations=migrations)
            migration_checkpoint.save()
            pprint(migrations)

        except Exception as e:
            raise CommandError(e)

