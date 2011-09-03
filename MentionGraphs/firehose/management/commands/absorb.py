from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    #args = '<poll_id poll_id ...>'
    help = 'Fetch data from the uberVU API'

    def handle(self, *args, **options):
        self.stdout.write('hello\n')
