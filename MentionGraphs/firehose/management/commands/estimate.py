from datetime import date, time, datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from MentionGraphs.firehose.crawl import do_api_call, to_epoch, end_of_day_epoch

class Command(BaseCommand):
    #args = '<poll_id poll_id ...>'
    help = 'Estimate volume of data for a given keyword'

    def handle(self, keyword, the_day, **kwargs):

        import logging
        l = logging.getLogger('MentionGraphs.firehose.crawl')
        l.setLevel(logging.INFO)
        l.addHandler(logging.StreamHandler(self.stderr))

        day = date(*map(int, the_day.split('-')))
        t0 = to_epoch(datetime.combine(day, time()))
        t = end_of_day_epoch(day)

        results = do_api_call(keyword, t0, t)

        if not results:
            print "no data"

        elif len(results) == 1:
            print "1 per day"

        else:
            interval = results[0]['published'] - results[-1]['published']
            count = int(len(results) * (24.0 * 60 * 60) / interval) + 1
            print "%d per day" % count
