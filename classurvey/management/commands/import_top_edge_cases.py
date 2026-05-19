from django.core.management.base import BaseCommand
from classurvey.models import TopLevel, TopLevelEdgeCase

import csv
import os


class Command(BaseCommand):
    help = 'Import top-level edge case definitions from a CSV file.'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **options):
        path = options['path'][0]
        if not os.path.exists(path):
            self.stderr.write(self.style.ERROR(f"The path '{path}' does not exist."))
            return

        self.stdout.write(self.style.SUCCESS(f"Importing edge cases from '{path}'."))
        created_count, skipped_count = import_top_edge_cases_csv(path, self)
        self.stdout.write(
            self.style.SUCCESS(
                f'Done. Created {created_count} edge cases, skipped {skipped_count} rows.'
            )
        )


def import_top_edge_cases_csv(file_path, command=None):
    required_columns = {'TopLevel', 'Definition'}
    created_count = 0
    skipped_count = 0

    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        if not reader.fieldnames:
            raise ValueError('CSV file is empty or missing header row.')

        missing_columns = required_columns - set(reader.fieldnames)
        if missing_columns:
            raise ValueError(
                'CSV is missing required columns: '
                + ', '.join(sorted(missing_columns))
            )

        for row_number, row in enumerate(reader, start=2):
            top_level_name = (row.get('TopLevel') or '').strip()
            definition = (row.get('Definition') or '').strip()

            if not top_level_name or not definition:
                skipped_count += 1
                if command:
                    command.stderr.write(
                        command.style.WARNING(
                            f'Skipping row {row_number}: TopLevel/Definition cannot be empty.'
                        )
                    )
                continue

            top_level = TopLevel.objects.filter(top_level_name=top_level_name).first()
            if top_level is None:
                skipped_count += 1
                if command:
                    command.stderr.write(
                        command.style.WARNING(
                            f"Skipping row {row_number}: TopLevel '{top_level_name}' not found."
                        )
                    )
                continue

            _, created = TopLevelEdgeCase.objects.get_or_create(
                top_level=top_level,
                definition=definition,
            )
            if created:
                created_count += 1
            else:
                skipped_count += 1

    return created_count, skipped_count
