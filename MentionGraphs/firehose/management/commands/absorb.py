from django.core.management.base import BaseCommand, CommandError
from MentionGraphs.firehose.crawl import index_day

class Command(BaseCommand):
    #args = '<poll_id poll_id ...>'
    help = 'Fetch data from the uberVU API'

    def handle(self, keyword, day, **kwargs):
        from pprint import pprint
        from datetime import date, timedelta
        import logging
        l = logging.getLogger('MentionGraphs.firehose.crawl')
        l.setLevel(logging.INFO)
        l.addHandler(logging.StreamHandler(self.stderr))

        day = date(*map(int, day.split('-')))
        pprint(dict(index_day(keyword, day, timedelta(hours=1))))
