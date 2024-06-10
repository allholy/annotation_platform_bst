from django.core.management.base import BaseCommand
from classurvey.views import data_for_export

from datetime import datetime
import json


from django.core.management.base import BaseCommand
from datetime import datetime
import json

class Command(BaseCommand):
    help = 'Export sound annotations to a local JSON file'

    def handle(self, *args, **kwargs):
        current_date = datetime.now().strftime('%y%m%d')
        file_path = f'/code/classurvey/data/data_{current_date}.json'
        print(file_path)
        data = data_for_export()
        
        # Serialize datetime objects to strings
        def json_serial(obj):
            if isinstance(obj, datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            raise TypeError("Type not serializable")

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4, default=json_serial)
        
        self.stdout.write(self.style.SUCCESS(f'Data successfully exported to {file_path}'))

