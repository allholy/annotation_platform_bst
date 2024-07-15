from django.core.management.base import BaseCommand
from classurvey.models import TestSound, SoundAnswer

import csv
import os


class Command(BaseCommand):
    # The data is in csv file. Its path is an argument.
    help = 'Path for file with already annotate sounds.'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)
        # parser.add_argument('-annotatorname', type=str, help='Name of annotator')
        # parser.add_argument('-annotatorid', type=str, help='Name of annotator')

    def handle(self, *args, **options):
        path = options['path'][0]
        if not os.path.exists(path):
            self.stderr.write(self.style.ERROR(f"The path '{path}' does not exist."))
            return
            
        self.stdout.write(self.style.SUCCESS(f"Importing data from '{path}'."))

        import_sounds_with_annotations_csv(path)


def import_sounds_with_annotations_csv(file_path):
    '''
    Import sound data with annotations from csv file.
    '''
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sound, _ = TestSound.objects.get_or_create(
                sound_id=row['sound_id'],
                sound_class=row['class'],
                sound_group=row['group'],
            )

            SoundAnswer.objects.get_or_create(
                test_sound = sound,
                chosen_class=row['chosen_class'],
                confidence=row['confidence'],
                comment=row['comment']
                )