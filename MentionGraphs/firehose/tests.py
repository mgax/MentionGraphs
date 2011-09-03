from StringIO import StringIO
import json
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

        mentions = list(do_api_call('python', 'twitter'))

        self.assertEqual(mentions, [item1])
