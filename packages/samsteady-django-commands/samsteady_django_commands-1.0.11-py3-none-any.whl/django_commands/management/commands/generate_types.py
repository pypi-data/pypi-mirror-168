import fileinput

import humps
from django.core.management import BaseCommand
from django_typomatic import generate_ts

fn = './api_types.ts'


class Command(BaseCommand):

    def handle(self, *args, **options):
        generate_ts(fn)
        for line in fileinput.input(fn, inplace=True):
            line = line.replace('Serializer {', ' {')
            line = line.replace('interface ', 'interface IApi')
            if ':' in line:
                split_lines = line.split(':')
                var_name = humps.camelize(split_lines[0])
                value = split_lines[1]
                line = var_name + ':' + value
            line = line.replace('\n', '')
            print(line)

