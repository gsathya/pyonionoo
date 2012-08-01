import sys
import datetime
import pyonionoo.database as database

import cyclone.escape
import cyclone.web

from twisted.internet import defer, reactor
from twisted.python import log

from pyonionoo.parser import Router

ARGUMENTS = ['type', 'running', 'search', 'lookup', 'country', 'order', 'offset', 'limit']

class SummaryHandler(cyclone.web.RequestHandler):
    def get(self, foo):

        user_arguments = self.request.arguments
        routers = database.get_summary_router(user_arguments)

        response = {}
        relays, bridges = [], []
        filtered_relays, filtered_bridges, relay_timestamp, bridge_timestamp = routers
        
        for (src, dest) in [(filtered_relays, relays),(filtered_bridges, bridges)]:
            for router in src:
                dest.append({'n': router.nickname, 'f': router.fingerprint, 'a': [router.address], 'r': router.is_running})


        if relays:
            response['relays'] = relays
            response['relays_published'] = relay_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        if bridges:
            response['bridges'] = bridges
            response['bridges_published'] = bridge_timestamp.strftime("%Y-%m-%d %H:%M:%S")

        self.write(response)
