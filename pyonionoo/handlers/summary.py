import sys
import datetime

import cyclone.escape
import cyclone.web

from twisted.internet import threads, defer, reactor
from twisted.python import log

import pyonionoo.handlers.arguments as arguments
import pyonionoo.database as database
from pyonionoo.parser import Router

ARGUMENTS = ['type', 'running', 'search', 'lookup', 'country', 'order', 'offset', 'limit']

class SummaryHandler(cyclone.web.RequestHandler):

    @defer.inlineCallbacks
    def get(self):
        """
        Respond to a GET request.  We construct the response in a different
        thread to avoid blocking.  deferToThread returns a Deferred object,
        which we can yield immediately; Cyclone then knows to invoke get()
        again when _get_results has finished, and resopnse will be the
        return value of _get_results (i.e., the dictionary of results).
        """
        d = threads.deferToThread(self._get_results)
        response = yield d
        self.write(response)
        
    def _get_results(self):

        user_arguments = self.request.arguments
        routers = database.get_summary_routers(**arguments.parse(user_arguments))

        response = {}
        relays, bridges = [], []
        filtered_relays, filtered_bridges, relay_timestamp, bridge_timestamp = routers

        for (src, dest) in ((filtered_relays, relays), 
                (filtered_bridges, bridges)):
            for router in src:
                dest.append({
                    'n' : router['nickname'],
                    'f' : router['fingerprint'],
                    'r' : bool(router['running'])
                })

        if relays:
            response['relays'] = relays
            response['relays_published'] = relay_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        if bridges:
            response['bridges'] = bridges
            response['bridges_published'] = bridge_timestamp.strftime("%Y-%m-%d %H:%M:%S")

        return response

