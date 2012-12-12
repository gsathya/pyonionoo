from itertools import cycle

import cyclone.httpclient

from utils import *

from cyclone.escape import json_decode
from cyclone.httputil import url_concat
from twisted.internet import defer
from twisted.trial import unittest

host = "localhost"
port = 8888
base_url = "http://%s:%s" % (host, port)
content_type = 'application/json'
response_code = 200

class TestUnparameterizedRequests(unittest.TestCase):
    def setUp(self):
        self.relays, self.bridges = {}, {}

        self.relays['nicknames'] = ['sumkledi', 'Unnamed']
        self.bridges['nicknames'] = ['TSPIDER', 'obfsabox']

        self.relays['fingerprint'] = ['0013D22389CD50D0B784A3E4061CB31E8CE8CEB5', '0036D8A9212508D2C963B4BA965FF33FEF9842EB']
        self.bridges['fingerprint'] = ['FF62690E83AA32852E2079AC6A65D65953E57498', 'FFDE7B45014B150E61B26DC72764386D416E8956']

        self.relays['running'] = [True, True]
        self.bridges['running'] = [True, True]
        
    @defer.inlineCallbacks
    def test_summary(self):
        url = "%s/%s" % (base_url, 'summary')
        response = yield cyclone.httpclient.fetch(url)
        data = json_decode(response.body)

        self.assertEqual(4, number_of_relays(data)+number_of_bridges(data))
        self.assertEqual("2012-07-03 07:00:00", data['relays_published'])
        self.assertEqual("2012-07-03 07:07:04", data['bridges_published'])

        # check if nicknames are alphanumeric
        self.assertEqual([], filter(lambda x: not x['n'].isalnum(), data['relays']))
        self.assertEqual([], filter(lambda x: not x['n'].isalnum(), data['bridges']))

        # check if nicknames are 1-19 chars
        self.assertEqual([], filter(lambda x: not 0<len(x['n'])<20, data['relays']))
        self.assertEqual([], filter(lambda x: not 0<len(x['n'])<20, data['bridges']))

        # check if nicknames are correct
        self.assertEqual([], filter(lambda (x, y): x['n']!=y, zip(data['relays'], self.relays['nicknames'])))
        self.assertEqual([], filter(lambda (x, y): x['n']!=y, zip(data['bridges'], self.bridges['nicknames'])))

        # check if fp are correct
        self.assertEqual([], filter(lambda (x, y): x['f']!=y, zip(data['relays'], self.relays['fingerprint'])))
        self.assertEqual([], filter(lambda (x, y): x['f']!=y, zip(data['bridges'], self.bridges['fingerprint'])))
        
        # check if fp is all upper case
        self.assertEqual([], filter(lambda x: not x['f'].isupper(), data['relays']))
        self.assertEqual([], filter(lambda x: not x['f'].isupper(), data['bridges']))
        
        # check if fp is 40 chars
        self.assertEqual([], filter(lambda x: len(x['f'])!=40, data['relays']))
        self.assertEqual([], filter(lambda x: len(x['f'])!=40, data['bridges']))

        # check if ips are equal
        pass

        # check if ipv6 ips are lowercase
        pass

        # check if running fields are correct
        self.assertEqual([], filter(lambda (x, y): x['r']!=y, zip(data['relays'], self.relays['running'])))
        self.assertEqual([], filter(lambda (x, y): x['r']!=y, zip(data['bridges'], self.bridges['running'])))
        
        # check no additional fields are present - change to 4 when test data is updated
        self.assertEqual([], filter(lambda (x, y): len(x)!=y, zip(data['relays'], cycle([3]))))
        self.assertEqual([], filter(lambda (x, y): len(x)!=y, zip(data['bridges'], cycle([3]))))
