from django.conf import settings
import urllib
import json
import time
from datetime import timedelta
from collections import defaultdict
import logging

log = logging.getLogger(__name__)

API_KEY = settings.UBERVU_API_KEY
STATS_FIELDS = ['language', 'generator', 'sentiment']
FIELDS = STATS_FIELDS + ['published']
RESPONSE_LIMIT = 100


def date_epoch(date):
    return int(time.mktime(date.timetuple()))

def end_of_day_epoch(date):
    return date_epoch(date+timedelta(days=1)) - 1



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
    log.info("Crawling mentions for %r on %s (%r -> %r)",
             keyword, target_date, since, until)

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

        until = mention['published'] - 1

    log.info("... finished counting %d mentions", total_mentions)

def index_day(keyword, target_date):
    t0 = date_epoch(target_date)
    t = end_of_day_epoch(target_date)
    stats = defaultdict(int)

    for mention in mention_stream_for_interval(t0, t):
        for field in STATS_FIELDS:
            stats[field, mention[field]] += 1

    return stats
