import sys
import pyonionoo.get_router as get_router

import cyclone.escape
import cyclone.web

from twisted.internet import defer, reactor
from twisted.python import log

from pyonionoo.parser import Router

ARGUMENTS = ['type', 'running', 'search', 'lookup', 'country', 'order', 'offset', 'limit']

class SummaryHandler(cyclone.web.RequestHandler):
    def get(self, foo):
        return_relays, return_bridges= True, True
        hex_fingerprint = None
        is_running, return_running = False, False
        return_country, return_search = False, False

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
                relay_info["n"] = router.nickname
                relay_info["f"] = router.fingerprint
                relay_info["a"] = [router.address]
                relay_info["r"] = router.is_running
                if router.exit_addresses:
                    relay_info["a"].extend(router.exit_addresses)
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
                bridge_info["n"] = router.nickname
                bridge_info["f"] = router.fingerprint
                bridge_info["a"] = [router.address]
                bridge_info["r"] = router.is_running
                if router.exit_addresses:
                    bridge_info["a"].extend(router.exit_addresses)
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