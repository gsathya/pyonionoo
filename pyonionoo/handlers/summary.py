import sys
import json
import datetime
import pyonionoo.get_router as get_router

import cyclone.escape
import cyclone.web

from twisted.internet import defer, reactor
from twisted.python import log

from pyonionoo.parser import Router

ARGUMENTS = ['type', 'running', 'search', 'lookup', 'country', 'order', 'offset', 'limit']

class SummaryHandler(cyclone.web.RequestHandler):
    def get(self, foo):

        user_arguments = self.request.arguments
        routers = get_router.get_routers(user_arguments)
        
        response = {}
        relays, bridges = [], []
        filtered_relays, filtered_bridges, relay_timestamp, bridge_timestamp = routers
        if filtered_relays:
            for relay in filtered_relays:
                relay_info = {}
                relay_info["n"] = relay.nickname
                relay_info["f"] = relay.fingerprint
                relay_info["a"] = [relay.address]
                relay_info["r"] = relay.is_running
                relays.append(relay_info)
        if filtered_bridges:
            for bridge in filtered_bridges:
                bridge_info = {}
                bridge_info["n"] = bridge.nickname
                bridge_info["f"] = bridge.fingerprint
                bridge_info["a"] = [bridge.address]
                bridge_info["r"] = bridge.is_running
                bridges.append(bridge_info)

        if relays:
            response['relays'] = relays
            response['relays_published'] = relay_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        if bridges:
            response['bridges'] = bridges
            response['bridges_published'] = bridge_timestamp.strftime("%Y-%m-%d %H:%M:%S")

        self.write(response)
