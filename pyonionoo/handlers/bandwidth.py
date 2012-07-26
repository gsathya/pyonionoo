import sys
import pyonionoo.get_router as get_router

import cyclone.escape
import cyclone.web

from pyonionoo.parser import Router

ARGUMENTS = ['type', 'running', 'search', 'lookup', 'country', 'order', 'offset', 'limit']

class BandwidthHandler(cyclone.web.RequestHandler):
    def get(self, foo):
        return_relays, return_bridges= True, True
        hex_fingerprint = None
        is_running, return_running = False, False
        return_country, return_search = False, False

        routers = get_router.get_routers()

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

        for router in routers:
            if router.is_relay and return_relays:
                relay_info = {}
                relay_info["fingerprint"] = router.fingerprint
                write_history_info = {}
                3_day_info = {}
                1_week_info = {}
                1_month_info = {}
                3_months_info = {}
                1_year_info = {}
                5_years_info = {}
