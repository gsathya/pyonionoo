import sys
import datetime

import cyclone.escape
import cyclone.web

from twisted.internet import defer, reactor
from twisted.python import log

import pyonionoo.handlers.arguments as arguments
import pyonionoo.database as database
from pyonionoo.parser import Router

ARGUMENTS = ['type', 'running', 'search', 'lookup', 'country', 'order', 'offset', 'limit']

class SummaryHandler(cyclone.web.RequestHandler):
    def get(self, foo):

        user_arguments = self.request.arguments
        routers = database.get_summary_routers(**arguments.parse(user_arguments))

        response = {}
        relays, bridges = [], []
        filtered_relays, filtered_bridges, relay_timestamp, bridge_timestamp = routers

        for (router_type, nickname, fingerprint, running, country_code, time_published, consensus_weight) in filtered_relays:
            if running == 0:
                running_str = 'false'
            if running == 1:
                running_str = 'true' 
            relays.append({'n': nickname, 'f': fingerprint, 'r': running_str})

        for (router_type, nickname, fingerprint, running, country_code, time_published, consensus_weight) in filtered_bridges:   
            if running == 0:
                running_str = 'false'
            if running == 1:
                running_str = 'true' 
            bridges.append({'n': nickname, 'f': fingerprint, 'r': running_str})

        if relays:
            response['relays'] = relays
            response['relays_published'] = relay_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        if bridges:
            response['bridges'] = bridges
            response['bridges_published'] = bridge_timestamp.strftime("%Y-%m-%d %H:%M:%S")

        self.write(response)

