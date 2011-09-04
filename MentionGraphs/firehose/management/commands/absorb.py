from datetime import date, timedelta
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from MentionGraphs.firehose.crawl import MentionCounter
from MentionGraphs.firehose.models import save_data

class Command(BaseCommand):
    #args = '<poll_id poll_id ...>'
    help = 'Fetch data from the uberVU API'

    def handle(self, keyword, day0, ndays, **kwargs):

        import logging
        l = logging.getLogger('MentionGraphs.firehose.crawl')
        l.setLevel(logging.INFO)
        l.addHandler(logging.StreamHandler(self.stderr))

        day0 = date(*map(int, day0.split('-')))
        resolution = timedelta(hours=1)

        for c in range(int(ndays)):
            day = day0 + timedelta(days=c)
            data = MentionCounter(keyword, resolution).count(day)
            with transaction.commit_on_success():
                save_data(keyword, data)
