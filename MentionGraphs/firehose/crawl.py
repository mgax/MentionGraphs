from django.conf import settings
import urllib
import json
from time import mktime
from datetime import datetime, time, timedelta
from collections import defaultdict
import logging

log = logging.getLogger(__name__)

API_KEY = settings.UBERVU_API_KEY
STATS_FIELDS = ['language', 'generator', 'sentiment']
FIELDS = STATS_FIELDS + ['published']
RESPONSE_LIMIT = 100


def to_epoch(date):
    return int(mktime(date.timetuple()))

def end_of_day_epoch(date):
    return to_epoch(date+timedelta(days=1)) - 1



def do_api_call(keyword, since, until):
    base = 'http://api.contextvoice.com/1.2/mentions/search/mongo/?'
    url = base + urllib.urlencode({
        'q': keyword,
        'apikey': API_KEY,
        'count': RESPONSE_LIMIT,
        'since': since,
        'until': until,
    })

    response = urllib.urlopen(url)
    data = json.load(response)
    response.close()

    for mention in data['results']:
        yield {k: mention.get(k, None) for k in FIELDS}

def mention_stream_for_interval(keyword, since, until):
    log.info("Crawling mentions for %r (%r -> %r)", keyword, since, until)

    total_mentions = 0
    while True:
        count = 0
        mentions = do_api_call(keyword, since, until)
        for count, m in enumerate(mentions, start=1):
            yield m

        if not count:
            break

        total_mentions += count
        log.info("... %d mentions from %r", count, until)

        until = m['published'] - 1

    log.info("... finished counting %d mentions", total_mentions)


class MentionCounter(object):

    def __init__(self, keyword, resolution):
        self.keyword = keyword
        self.resolution = resolution

    def stream_for_day(self, day):
        t0 = to_epoch(datetime.combine(day, time()))
        t = end_of_day_epoch(day)
        return mention_stream_for_interval(self.keyword, t0, t)

    def count(self, day):
        day_start = datetime.combine(day, time())
        t0 = to_epoch(day_start)
        res_seconds = self.resolution.total_seconds()
        n_buckets = int(24*60*60/res_seconds)
        day_buckets = [defaultdict(int) for i in range(n_buckets)]

        for mention in self.stream_for_day(day):
            time_in_day = mention['published'] - t0
            bucket = day_buckets[int(time_in_day / res_seconds)]
            for field in STATS_FIELDS:
                bucket[field, mention[field]] += 1

        return {day_start + self.resolution * i: day_buckets[i]
                for i in range(n_buckets)}
