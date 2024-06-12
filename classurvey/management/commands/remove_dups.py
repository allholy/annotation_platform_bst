from django.core.management.base import BaseCommand
from django.db.models import Count
from classurvey.models import SoundAnswer


class Command(BaseCommand):
    help = 'Removes duplicates from SoundAnswer and keeps the latest according to the date created.'

    def handle(self, *args, **kwargs):
        # Get a queryset of duplicate records based on the 'test_sound_id' field
        duplicate_records = SoundAnswer.objects.values('test_sound_id').annotate(count=Count('test_sound_id')).filter(count__gt=1)
        
        total_duplicates = duplicate_records.count()
        
        # Show the number of duplicates found
        self.stdout.write(self.style.SUCCESS(f'Total duplicate sound ids found: {total_duplicates}'))
        
        if total_duplicates == 0:
            self.stdout.write(self.style.SUCCESS('No duplicates to remove. Operation cancelled.'))
            return

        # Prompt user for confirmation
        confirmation = input('Do you want to delete the duplicates? (y/n): ').lower()
        
        if confirmation != 'y':
            self.stdout.write(self.style.SUCCESS('Operation cancelled.'))
            return
        
        total_deleted = 0
        
        for record in duplicate_records:
            # Get the earliest of each duplicate record
            # TODO: chosse all except of the first
            duplicates_to_delete = SoundAnswer.objects.filter(test_sound_id=record['test_sound_id']).order_by('date_created')[:1]
            print(SoundAnswer.objects.filter(test_sound_id=record['test_sound_id']).order_by('-date_created'))
            print(duplicates_to_delete)
            
            total_deleted += len(duplicates_to_delete)
            
            # Delete duplicates individually
            for duplicate in duplicates_to_delete:
                duplicate.delete()


        self.stdout.write(self.style.SUCCESS(f'Duplicates removed successfully. Total deleted: {total_deleted}'))