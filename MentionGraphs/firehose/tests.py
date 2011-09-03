from StringIO import StringIO
import json
from datetime import date, time, datetime, timedelta
from django.test import TestCase
from mock import patch


def _mention(published, language='english', generator='twitter', sentiment=None):
    return {
        'language': language,
        'generator': generator,
        'sentiment': sentiment,
        'published': published,
    }

class ApiCallTest(TestCase):

    def setUp(self):
        import urllib
        self._urllib_mock = patch('MentionGraphs.firehose.crawl.urllib')
        mock_urllib = self._urllib_mock.start()
        self.mock_urlopen = mock_urllib.urlopen
        mock_urllib.urlencode = urllib.urlencode

    def tearDown(self):
        self._urllib_mock.stop()

    def set_api_response(self, mentions):
        data = {
            'count': len(mentions),
            'total': len(mentions),
            'results': mentions,
        }
        self.mock_urlopen.return_value = StringIO(json.dumps(data))

    def test_api_call(self):
        from crawl import do_api_call
        item1 = _mention(1315051701)
        self.set_api_response([item1])

        mentions = list(do_api_call('python', 1315051000, 1315052000))

        self.assertEqual(mentions, [item1])

class CrawlingTest(TestCase):

    def setUp(self):
        self._api_mock = patch('MentionGraphs.firehose.crawl'
                               '.mention_stream_for_interval')
        self._mock_call = self._api_mock.start()

    def tearDown(self):
        self._api_mock.stop()

    def api_fixture(self, data):
        self._mock_call.return_value = data

    def test_crawl_one_day_one_call(self):
        from crawl import index_day
        self.api_fixture([
            _mention(1315051701, 'english', 'twitter', 'neutral'),
            _mention(1315051704, 'german', 'twitter', 'positive'),
            _mention(1315051708, 'english', 'facebook', 'negative'),
        ])

        stats = index_day('python', date(2011, 9, 3), timedelta(days=1))

        bucket = stats.values()[0]

        self.assertEqual(bucket['language', 'english'], 2)
        self.assertEqual(bucket['language', 'german'], 1)
        self.assertEqual(bucket['generator', 'twitter'], 2)
        self.assertEqual(bucket['generator', 'facebook'], 1)
        self.assertEqual(bucket['sentiment', 'negative'], 1)
        self.assertEqual(bucket['sentiment', 'neutral'], 1)
        self.assertEqual(bucket['sentiment', 'positive'], 1)

    def test_split_into_intervals(self):
        from crawl import index_day, to_epoch

        day = date(2011, 9, 3)
        eday = to_epoch(day)

        self.api_fixture([
            _mention(eday + 60 * 20, 'english'),
            _mention(eday + 60 * 30, 'english'),
            _mention(eday + 60 * 40, 'german'),
            _mention(eday + 60 * 90, 'german'),
            _mention(eday + 60 * 100, 'german'),
            _mention(eday + 60 * 110, 'french'),
        ])

        stats = index_day('python', day, timedelta(hours=1))

        bucket0 = stats[datetime.combine(day, time())]
        self.assertEqual(bucket0['language', 'english'], 2)
        self.assertEqual(bucket0['language', 'german'], 1)

        bucket1 = stats[datetime.combine(day, time(1))]
        self.assertEqual(bucket1['language', 'german'], 2)
        self.assertEqual(bucket1['language', 'french'], 1)
