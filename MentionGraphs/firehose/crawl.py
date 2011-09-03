from django.conf import settings
import urllib
import json
from collections import defaultdict

API_KEY = settings.UBERVU_API_KEY
STATS_FIELDS = ['language', 'generator', 'sentiment']
FIELDS = STATS_FIELDS + ['published']


def do_api_call(keyword):
    base = 'http://api.contextvoice.com/1.2/mentions/search/mongo/?'
    url = base + urllib.urlencode({
        'q': keyword,
        'apikey': API_KEY,
    })

    response = urllib.urlopen(url)
    data = json.load(response)
    response.close()

    for mention in data['results']:
        yield {k: mention.get(k, None) for k in FIELDS}

def index_day(keyword, target_date):
    stats = defaultdict(int)

    for mention in do_api_call(keyword):
        for field in STATS_FIELDS:
            stats[field, mention[field]] += 1

    return stats
