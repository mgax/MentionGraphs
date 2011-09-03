from StringIO import StringIO
import json
from datetime import date
from django.test import TestCase
from mock import patch


def _mention(language, generator, sentiment, published):
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
        item1 = _mention('english', 'twitter', 'neutral', 1315051701)
        self.set_api_response([item1])

        mentions = list(do_api_call('python', 1315051000, 1315052000))

        self.assertEqual(mentions, [item1])

class CrawlingTest(TestCase):

    def setUp(self):
        self._api_mock = patch('MentionGraphs.firehose.crawl.do_api_call')
        self._mock_call = self._api_mock.start()

    def tearDown(self):
        self._api_mock.stop()

    def api_fixture(self, data):
        data = data + [[]]
        self._mock_call.side_effect = lambda *args: data.pop

    def test_crawl_one_day_one_call(self):
        from nose import SkipTest; raise SkipTest
        from crawl import index_day
        self.api_fixture([
            _mention('english', 'twitter', 'neutral', 1315051701),
            _mention('german', 'twitter', 'positive', 1315051704),
            _mention('english', 'facebook', 'negative', 1315051708),
        ])

        stats = index_day('python', date(2011, 9, 3))

        self.assertEqual(stats['language', 'english'], 2)
        self.assertEqual(stats['language', 'german'], 1)
        self.assertEqual(stats['generator', 'twitter'], 2)
        self.assertEqual(stats['generator', 'facebook'], 1)
        self.assertEqual(stats['sentiment', 'negative'], 1)
        self.assertEqual(stats['sentiment', 'neutral'], 1)
        self.assertEqual(stats['sentiment', 'positive'], 1)
