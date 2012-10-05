import cyclone.httpclient

from summary_responses import *
from cyclone.escape import json_decode
from cyclone.httputil import url_concat
from twisted.internet import defer
from twisted.trial import unittest

host = "localhost"
port = 8888
url = "http://%s:%s/%s" % (host, port, 'summary')

# fixme: passing self is a bad idea
def check_correct_response(self, response, expected):
    self.assertEqual(response.code, 200)
    self.assertEqual(response.headers['Content-Type'][0], 'application/json')
    # check if valid json
    json_decode(response.body)
    self.assertEqual(response.body, expected)

# xxx: passing self is a bad idea
def check_incorrect_response(self, response, expected):
    self.assertEqual(response.code, 400)
    self.assertEqual(response.body, expected)

class TestSummaryDocuments(unittest.TestCase):
    # check correct response of full summary
    @defer.inlineCallbacks
    def test_summary(self):
        response = yield cyclone.httpclient.fetch(url)
        check_correct_response(self, response, FULL_SUMMARY)

    # check correct response of TYPE argument where TYPE=relay
    @defer.inlineCallbacks
    def test_relay_type(self):
        params = {'type': 'relay'}
        response = yield cyclone.httpclient.fetch(url_concat(url, params))
        check_correct_response(self, response, RELAY_SUMMARY)

    # check correct response of TYPE argument where TYPE=bridge
    @defer.inlineCallbacks
    def test_bridge_type(self):
        params = {'type': 'bridge'}
        response = yield cyclone.httpclient.fetch(url_concat(url, params))
        check_correct_response(self, response, BRIDGE_SUMMARY)

    # check correct response of RUNNING argument where RUNNING=true
    @defer.inlineCallbacks
    def test_running_true(self):
        params = {'running': 'true'}
        response = yield cyclone.httpclient.fetch(url_concat(url, params))
        check_correct_response(self, response, RUNNING_TRUE)

    # check correct response of RUNNING argument where RUNNING=false
    @defer.inlineCallbacks
    def test_running_false(self):
        params = {'running': 'false'}
        response = yield cyclone.httpclient.fetch(url_concat(url, params))
        check_correct_response(self, response, RUNNING_FALSE)

    # check correct response of LOOKUP argument where LOOKUP is hashed fingerprint
    @defer.inlineCallbacks
    def test_lookup_hashed_fp(self):
        hashed_fp = "0014A2055278DB3EB0E59EA701741416AF185558"
        params = {'lookup': hashed_fp}
        response = yield cyclone.httpclient.fetch(url_concat(url, params))
        check_correct_response(self, response, LOOKUP_RESULT_HASHED_FINGERPRINT)

    # check incorrect response of LOOKUP argument where LOOKUP is fingerprint
    @defer.inlineCallbacks
    def test_lookup_fp(self):
        fp = "0013D22389CD50D0B784A3E4061CB31E8CE8CEB5"
        params = {'lookup': fp}
        response = yield cyclone.httpclient.fetch(url_concat(url, params))
        check_correct_response(self, response, LOOKUP_RESULT_FINGERPRINT)

    # check correct response of LOOKUP argument where LOOKUP is lower case fingerprint
    @defer.inlineCallbacks
    def test_lookup_case_insensitive_fp(self):
        fp = "0013D22389CD50D0B784A3E4061CB31E8CE8CEB5"
        params = {'lookup': fp.lower()}
        response = yield cyclone.httpclient.fetch(url_concat(url, params))
        check_correct_response(self, response, LOOKUP_RESULT_FINGERPRINT)

    # check incorrect response of LOOKUP argument where LOOKUP is <40 chars
    @defer.inlineCallbacks
    def test_lookup_incorrect(self):
        fp = "0014A20552"
        params = {'lookup': fp}
        response = yield cyclone.httpclient.fetch(url_concat(url, params))
        check_incorrect_response(self, response, BAD_REQUEST)

    # check correct response of COUNTRY argument
    @defer.inlineCallbacks
    def test_country(self):
        country = "ru"
        params = {'country': country}
        response = yield cyclone.httpclient.fetch(url_concat(url, params))
        check_correct_response(self, response, COUNTRY_RESULT)

    # check correct response of COUNTRY argument where COUNTRY is upper case
    @defer.inlineCallbacks
    def test_country_case_insensitive(self):
        country = "ru"
        params = {'country': country.upper()}
        response = yield cyclone.httpclient.fetch(url_concat(url, params))
        check_correct_response(self, response, COUNTRY_RESULT)

    # check incorrect response of COUNTRY argument
    @defer.inlineCallbacks
    def test_country_incorrect(self):
        country = "russia"
        params = {'country': country}
        response = yield cyclone.httpclient.fetch(url_concat(url, params))
        check_incorrect_response(self, response, BAD_REQUEST)

    # check correct response of COUNTRY argument where COUNTRY is upper case
    @defer.inlineCallbacks
    def test_offset(self):
        offset = 2
        params = {'offset': offset}
        response = yield cyclone.httpclient.fetch(url_concat(url, params))
        check_correct_response(self, response, OFFSET_RESULT)

    # check incorrect response of OFFSET argument where offset is an alphabet
    @defer.inlineCallbacks
    def test_offset_incorrect(self):
        offset = 'a'
        params = {'offset': offset}
        response = yield cyclone.httpclient.fetch(url_concat(url, params))
        check_incorrect_response(self, response, BAD_REQUEST)

    # check correct response of LIMIT
    @defer.inlineCallbacks
    def test_limit(self):
        limit = 2
        params = {'limit': limit}
        response = yield cyclone.httpclient.fetch(url_concat(url, params))
        check_correct_response(self, response, LIMIT_RESULT)

    # check correct response of LIMIT when used with OFFSET
    @defer.inlineCallbacks
    def test_limit_offset(self):
        limit = 2
        offset = 1
        params = {'limit': limit, 'offset':offset}
        response = yield cyclone.httpclient.fetch(url_concat(url, params))
        check_correct_response(self, response, LIMIT_OFFSET_RESULT)

    # check incorrect response of LIMIT
    @defer.inlineCallbacks
    def test_limit_incorrect(self):
        limit = 'a'
        params = {'limit': limit}
        response = yield cyclone.httpclient.fetch(url_concat(url, params))
        check_incorrect_response(self, response, BAD_REQUEST)

