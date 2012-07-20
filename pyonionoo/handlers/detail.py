import sys
import pyonionoo.get_router as get_router

import cyclone.escape
import cyclone.web

from twisted.internet import defer, reactor
from twisted.python import log

from pyonionoo.parser import Router

ARGUMENTS = ['type', 'running', 'search', 'lookup', 'country', 'order', 'offset', 'limit']

class DetailHandler(cyclone.web.RequestHandler):
    def get(self, foo):
        return_relays, return_bridges = True, True
        is_running,return_running = False, False
        hex_fingerprint = None
        return_country = False

        routers = get_router.get_routers('/home/mchang01/HFOSS2012/pyonionoo/pyonionoo/summary')

        for argument in self.request.arguments.iterkeys():
            if argument in ARGUMENTS:
                #TODO - order, offset, limit
                if argument == "running":
                    return_running = True
                    value = self.get_argument(argument)
                    if value == "true":
                        is_running = True
                    if value == "false":
                        is_running = False
                if argument == "type":
                    value = self.get_argument(argument)
                    if value == "relay":
                        return_bridges = False
                    if value == "bridge":
                        return_relays = False
                if argument == "lookup":
                    hex_fingerprint = self.get_argument(argument)
                if argument == "country":
                    value = self.get_argument(argument)
                    return_country = True
                    country_code = value         
                if argument == "search":
                    search_input = self.get_argument(argument)
                    return_search = True                    
            else:
                raise ValueError("Invalid Argument!")

        response = {}
        relays, bridges = [], []

        for router in routers:
            if router.is_relay and return_relays:
                relay_info = {}
                relay_info["nickname"] = router.nickname
                relay_info["fingerprint"] = router.fingerprint
                relay_info["or_addresses"] = router.or_addresses
                relay_info["exit_addresses"] = router.exit_addresses
                #relay_info["dir_address"]
                relay_info["running"] = router.is_running
                relay_info["flags"] = router.flags
                relay_info["country"] = router.country_code
                #relay_info["country_name"]
                #relay_info["region_name"]
                #relay_info["city_name"]
                #relay_info["latitude"]
                #relay_info["longitude"]
                #relay_info["as_number"]
                #relay_info["as_name"]
                relay_info["consensus_weight"] = router.consensus_weight
                relay_info["host_name"] = router.hostname
                #relay_info["last_restarted"]
                #relay_info["advertised_bandwidth"]
                #relay_info["exit_policy"]
                #relay_info["contract"]
                #relay_info["platform"]
                #relay_info["family"]
                if router.exit_addresses:
                    relay_info["exit_addresses"].extend(router.exit_addresses)
                if hex_fingerprint:
                    if hex_fingerprint == router.fingerprint:
                        self.write({"relays":[relay_info]})
                        return
                if return_running:
                    if is_running:
                        if router.is_running:
                            relays.append(relay_info)
                    else:
                        if not router.is_running:
                            relays.append(relay_info)
                if return_country:
                    if router.country_code == country_code:
                        relays.append(relay_info)       
                if return_search:
                    if search_input in router.nickname:
                        relays.append(relay_info)
                    if search_input in router.fingerprint:
                        relays.append(relay_info)
                    if search_input in router.address:
                        relays.append(relay_info)
                else:
                    relays.append(relay_info)

            elif not router.is_relay and return_bridges:
                bridge_info = {}
                bridge_info["nickname"] = router.nickname
                bridge_info["hashed_fingerprint"] = router.fingerprint
                bridge_info["or_addresses"] = router.or_addresses
                bridge_info["running"] = router.is_running
                bridge_info["flags"] = router.flags
                #bridge_info["last_restarted"]
                #bridge_info["advertised_bandwidth"]
                #bridge_info["platform"]
                #bridge_info["pool_assignment"]
                if hex_fingerprint:
                    if hex_fingerprint == router.fingerprint:
                        self.write({"bridges":[bridge_info]})
                        return
                if return_running:
                    if is_running:
                        if router.is_running:
                            bridges.append(bridge_info)
                    else:
                        if not router.is_running:
                            bridges.append(bridge_info)
                if return_country:
                    if router.country_code == country_code:
                        relays.append(relay_info)            
                if return_search:
                    if search_input in router.nickname:
                        bridges.append(relay_info)
                    if search_input in router.fingerprint:
                        bridges.append(relay_info)
                    if search_input in router.address:
                        bridges.append(relay_info)                        
                else:
                    bridges.append(bridge_info)
        
        if relays:
            response['relays'] = relays
        if bridges:
            response['bridges'] = bridges

        self.write(response)         
