from django.core.management.base import BaseCommand
from django.db.models import Q
from classurvey.models import SoundAnswer


class Command(BaseCommand):
    help = 'Update empty user_id fields with a given string'

    def add_arguments(self, parser):
        parser.add_argument('new_id', type=str, help='The string to replace empty user_id fields with')

    def handle(self, *args, **kwargs):
        replacement_string = kwargs['new_id']
        users_to_update = SoundAnswer.objects.filter(Q(user_id='') | Q(user_id='-'))

        for user in users_to_update:
            user.user_id = replacement_string
            user.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully updated {users_to_update.count()} users'))
