import sys
import datetime
import pyonionoo.database as get_router

import cyclone.escape
import cyclone.web

from twisted.internet import threads, defer, reactor
from twisted.python import log

import pyonionoo.handlers.arguments as arguments
import pyonionoo.database as database
from pyonionoo.parser import Router

ARGUMENTS = ['type', 'running', 'search', 'lookup', 'country', 'order', 'offset', 'limit']

class BandwidthHandler(cyclone.web.RequestHandler):
    @defer.inlineCallbacks
    def get(self):
        d = threads.deferToThread(self._get_results)
        response = yield d
        self.write(response)

    def _get_results(self):
        user_arguments = self.request.arguments
        routers = database.get_bandwidth_routers(**arguments.parse(user_arguments))

        response = {}
        relays, bridges, relay_timestamp, bridge_timestamp = routers

        # response is a dict, so the order is not maintained. should the
        # values in the response be in a specific order?
        response['relays'] = relays
        response['relays_published'] = relay_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        response['bridges'] = bridges
        response['bridges_published'] = bridge_timestamp.strftime("%Y-%m-%d %H:%M:%S")

        return response
