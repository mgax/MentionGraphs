from datetime import date, timedelta
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import transaction
from MentionGraphs.firehose.crawl import CachingMentionCounter
from MentionGraphs.firehose.models import save_data

class Command(BaseCommand):
    #args = '<poll_id poll_id ...>'
    help = 'Fetch data from the uberVU API'

    def handle(self, keyword, day_start, n_days, n_workers, **kwargs):

        import logging
        l = logging.getLogger('MentionGraphs.firehose.crawl')
        l.setLevel(logging.INFO)
        l.addHandler(logging.StreamHandler(self.stderr))

        resolution = timedelta(hours=1)

        day0 = date(*map(int, day_start.split('-')))
        days = [day0 + timedelta(days=c) for c in range(int(n_days))]

        counter = CachingMentionCounter(
            keyword=keyword,
            resolution=resolution,
            cache_root=settings.FIREHOSE_DOWNLOAD_CACHE)

        import_with_workers(counter, days, int(n_workers))


def import_with_workers(counter, days, n_workers):
    from multiprocessing.pool import ThreadPool

    print "starting %d workers" % n_workers
    pool = ThreadPool(processes=n_workers)
    for day in days:
        pool.apply_async(import_one_day, (counter, day))
    print "jobs submitted, waiting..."
    pool.close()
    pool.join()
    print "done"


def import_one_day(counter, day):
    data = counter.count(day)
    with transaction.commit_on_success():
        save_data(counter.keyword, data)
