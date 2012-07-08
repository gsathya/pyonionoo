import sys

import cyclone.escape
import cyclone.web

from twisted.internet import defer, reactor
from twisted.python import log

from pyonionoo.parser import Router

ARGUMENTS = ['running', 'type', 'search', 'lookup', 'country', 'order', 'limit', 'offset']
class IndexHandler(cyclone.web.RequestHandler):
    def get(self, foo):
        return_relays, return_bridge = True, True
        routers = []
        hex_fingerprint = None
        #TODO - don't hardcode stuff
        with open('/Users/sathya/Documents/pyonionoo/pyonionoo/summary') as f:
            for line in f.readlines():
                router = Router(line)
                routers.append(router)
        
        for argument in self.request.arguments.iterkeys():
            if argument in ARGUMENTS:
                #TODO - running, search
                if argument == "type":
                    value = self.get_argument(argument)
                    if value == "relay":
                        return_bridges = False
                    if value == "bridge":
                        return_relays = False
                if argument == "lookup":
                    hex_fingerprint = self.get_argument(argument)
            else:
                #TODO - raise Exception
                pass
        
        response = {}
        relays = []
        for router in routers:
            if router.is_relay and return_relays:
                relay_info = {}
                relay_info["n"] = router.nickname
                relay_info["f"] = router.fingerprint
                relay_info["a"] = [router.address]
                if router.exit_addresses:
                    relay_info["a"].extend(router.exit_addresses)
                if hex_fingerprint:
                    if hex_fingerprint == router.fingerprint:
                        self.write({"relays":[relay_info]})
                        return
                #TODO - "r"
                relays.append(relay_info)
            elif not router.is_relay and return_bridges:
                bridge_info = {}
                bridge_info["n"] = router.nickname
                bridge_info["f"] = router.fingerprint
                bridge_info["a"] = [router.address]
                if router.exit_addresses:
                    bridge_info["a"].extend(router.exit_addresses)
                if hex_fingerprint:
                    if hex_fingerprint == router.fingerprint:
                        self.write({"relays":[bridge_info]})
                        return
                #TODO - "r"
                relays.append(bridge_info)
                
        if relays:
            response['relays'] = relays
        self.write(response)
