from django.conf import settings
import urllib
import json

API_KEY = settings.UBERVU_API_KEY
FIELDS = ['language', 'generator', 'sentiment', 'published']


def do_api_call(keyword, generator):
    base = 'http://api.contextvoice.com/1.2/mentions/search/mongo/?'
    url = base + urllib.urlencode({
        'q': keyword,
        'generator': generator,
        'apikey': API_KEY,
    })

    response = urllib.urlopen(url)
    data = json.load(response)
    response.close()

    for mention in data['results']:
        yield {k: mention.get(k, None) for k in FIELDS}
