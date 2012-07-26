import sys
import datetime
import pyonionoo.get_router as get_router

import cyclone.escape
import cyclone.web

from twisted.internet import defer, reactor
from twisted.python import log

from pyonionoo.parser import Router

ARGUMENTS = ['type', 'running', 'search', 'lookup', 'country', 'order', 'offset', 'limit']

class DetailHandler(cyclone.web.RequestHandler):
    def get(self, foo):

        user_arguments = self.request.arguments
        routers = get_router.get_routers(user_arguments)

        response = {}
        relays, bridges = [], []
        filtered_relays, filtered_bridges, relay_timestamp, bridge_timestamp = routers
        if filtered_relays:
            for relay in filtered_relays:
                relay_info = {}
                relay_info["nickname"] = relay.nickname
                relay_info["fingerprint"] = relay.fingerprint
                relay_info["or_addresses"] = relay.or_addresses
                relay_info["exit_addresses"] = relay.exit_addresses
                #relay_info["dir_address"]
                relay_info["running"] = relay.is_running
                relay_info["flags"] = relay.flags
                relay_info["country"] = relay.country_code
                #relay_info["country_name"]
                #relay_info["region_name"]
                #relay_info["city_name"]
                #relay_info["latitude"]
                #relay_info["longitude"]
                #relay_info["as_number"]
                #relay_info["as_name"]
                relay_info["consensus_weight"] = relay.consensus_weight
                relay_info["host_name"] = relay.hostname
                #relay_info["last_restarted"]
                #relay_info["advertised_bandwidth"]
                #relay_info["exit_policy"]
                #relay_info["contract"]
                #relay_info["platform"]
                #relay_info["family"]
                #-----------NEW FIELDS------------------------
                #relay_info["advertised_bandwidth_fraction]
                #relay_info["consensus_weight_fraction"]
                #relay_info["guard_probability"]
                #relay_info["middle_probability"]
                #relay_info["exit_probability"]
                relays.append(relay_info)
        if filtered_bridges:
            for bridge in filtered_bridges:
                bridge_info = {}
                bridge_info["nickname"] = bridge.nickname
                bridge_info["hashed_fingerprint"] = bridge.fingerprint
                bridge_info["or_addresses"] = bridge.or_addresses
                bridge_info["running"] = bridge.is_running
                bridge_info["flags"] = bridge.flags
                #bridge_info["last_restarted"]
                #bridge_info["advertised_bandwidth"]
                #bridge_info["platform"]
                #bridge_info["pool_assignment"]
                bridges.append(bridge_info)

        if relays:
            response['relays'] = relays
            response['relays_published'] = relay_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        if bridges:
            response['bridges'] = bridges
            response['bridges_published'] = bridge_timestamp.strftime("%Y-%m-%d %H:%M:%S")


        self.write(response)         
