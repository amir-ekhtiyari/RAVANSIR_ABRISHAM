"""
Create the PostgreSQL database from .env, build the tables and copy everything over from db.sqlite3.

    python manage.py setup_postgres

Safe to run again: the database is only created when missing and copied rows overwrite rows with the same id.
"""

import os
import tempfile
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import connections

# Rebuilt by Django itself on the new database – copying them would clash.
EXCLUDE = ['contenttypes', 'auth.permission', 'sessions', 'admin.logentry']


class Command(BaseCommand):
    help = 'Create the PostgreSQL database named in .env, migrate it and copy the data from db.sqlite3.'

    def add_arguments(self, parser):
        parser.add_argument('--sqlite', default=str(Path(settings.BASE_DIR) / 'db.sqlite3'),
                            help='SQLite file to copy from (default: db.sqlite3 next to manage.py).')
        parser.add_argument('--skip-data', action='store_true', help='Only create the database and the tables.')

    def handle(self, *args, **options):
        db = settings.DATABASES['default']
        if db['ENGINE'] != 'django.db.backends.postgresql':
            raise CommandError('Set POSTGRES_DB (and POSTGRES_USER / POSTGRES_PASSWORD) in .env first.')
        try:
            import psycopg
        except ImportError as exc:
            raise CommandError('Install the driver first: pip install "psycopg[binary]"') from exc

        name = db['NAME']
        self.stdout.write(f'1/3  Database "{name}" on {db["HOST"]}:{db["PORT"]} …')
        try:
            with psycopg.connect(host=db['HOST'], port=db['PORT'], user=db['USER'], password=db['PASSWORD'],
                                 dbname='postgres', autocommit=True, connect_timeout=10) as conn:
                exists = conn.execute('SELECT 1 FROM pg_database WHERE datname = %s', [name]).fetchone()
                if exists:
                    self.stdout.write('     already exists')
                else:
                    conn.execute(f'CREATE DATABASE "{name}" ENCODING \'UTF8\' TEMPLATE template0')
                    self.stdout.write(self.style.SUCCESS('     created'))
        except psycopg.OperationalError as exc:
            raise CommandError(f'Could not connect to PostgreSQL: {exc}') from exc

        self.stdout.write('2/3  Creating tables …')
        call_command('migrate', interactive=False, verbosity=0)
        self.stdout.write(self.style.SUCCESS('     done'))

        source = Path(options['sqlite'])
        if options['skip_data'] or not source.exists():
            self.stdout.write('3/3  No SQLite data copied.')
            return

        self.stdout.write(f'3/3  Copying data from {source.name} …')
        configured = connections.configure_settings({
            'default': settings.DATABASES['default'],
            'sqlite_source': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': str(source)},
        })
        connections.settings['sqlite_source'] = configured['sqlite_source']
        handle, dump = tempfile.mkstemp(suffix='.json')
        os.close(handle)
        try:
            call_command('dumpdata', database='sqlite_source', natural_foreign=True, natural_primary=True,
                         exclude=EXCLUDE, indent=None, output=dump, verbosity=0)
            call_command('loaddata', dump, verbosity=0)
        finally:
            connections['sqlite_source'].close()
            os.remove(dump)
        self.stdout.write(self.style.SUCCESS('     done – the site now runs on PostgreSQL.'))
