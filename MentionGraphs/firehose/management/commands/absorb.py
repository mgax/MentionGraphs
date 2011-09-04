from datetime import date, timedelta
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import transaction
from MentionGraphs.firehose.crawl import CachingMentionCounter
from MentionGraphs.firehose.models import save_data

class Command(BaseCommand):
    #args = '<poll_id poll_id ...>'
    help = 'Fetch data from the uberVU API'

    def handle(self, keyword, day_start, ndays, **kwargs):

        import logging
        l = logging.getLogger('MentionGraphs.firehose.crawl')
        l.setLevel(logging.INFO)
        l.addHandler(logging.StreamHandler(self.stderr))

        resolution = timedelta(hours=1)

        counter = CachingMentionCounter(
            keyword=keyword,
            resolution=resolution,
            cache_root=settings.FIREHOSE_DOWNLOAD_CACHE)

        day0 = date(*map(int, day_start.split('-')))

        for c in range(int(ndays)):
            day = day0 + timedelta(days=c)
            data = counter.count(day)
            with transaction.commit_on_success():
                save_data(keyword, data)
