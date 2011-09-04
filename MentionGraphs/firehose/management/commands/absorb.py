from datetime import date, timedelta
import logging
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import transaction
from MentionGraphs.firehose.crawl import CachingMentionCounter
from MentionGraphs.firehose.models import save_data


log = logging.getLogger(__name__)

class Command(BaseCommand):
    #args = '<poll_id poll_id ...>'
    help = 'Fetch data from the uberVU API'

    def handle(self, keyword, day_start, n_days, n_workers, **kwargs):

        stderr_handler = logging.StreamHandler(self.stderr)
        crawl_log = logging.getLogger('MentionGraphs.firehose.crawl')
        crawl_log.setLevel(logging.INFO)
        crawl_log.addHandler(stderr_handler)
        log.setLevel(logging.INFO)
        log.addHandler(stderr_handler)

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

    log.info("starting %d workers", n_workers)
    pool = ThreadPool(processes=n_workers)
    for day in days:
        pool.apply_async(import_one_day, (counter, day))
    log.info("jobs submitted, waiting...")
    pool.close()
    pool.join()
    log.info("jobs done")


def import_one_day(counter, day):
    data = counter.count(day)
    with transaction.commit_on_success():
        save_data(counter.keyword, data)
    log.info("saved datapoints for %r at %s", counter.keyword, day)
