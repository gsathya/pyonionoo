import cyclone.httpclient

from summary_responses import *
from cyclone.escape import json_decode
from cyclone.httputil import url_concat
from twisted.internet import defer
from twisted.trial import unittest

host = "localhost"
port = 8888
url = "http://%s:%s/%s" % (host, port, 'summary')
content_type = 'application/json'
response_code = 200

def check_correct_response(self, response, expected):
    self.assertEqual(response.code, 200)
    self.assertEqual(response.headers['Content-Type'][0], 'application/json')
    # check if valid json
    json_decode(response.body)
    self.assertEqual(response.body, expected)

class TestSummaryDocuments(unittest.TestCase):
    # check correct response of full summary
    @defer.inlineCallbacks
    def test_summary(self):
        response = yield cyclone.httpclient.fetch(url)
        self.assertEqual(response.code, response_code)
        self.assertEqual(response.headers['Content-Type'][0], 'application/json')
        data = json.loads(response.body)
        self.assertTrue(contains_required_fields(data))
