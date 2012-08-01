import sys
import pyonionoo.get_router as get_router

import cyclone.escape
import cyclone.web

from pyonionoo.parser import Router

ARGUMENTS = ['type', 'running', 'search', 'lookup', 'country', 'order', 'offset', 'limit']

class BandwidthHandler(cyclone.web.RequestHandler):
    def get(self, foo):
        """
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
            """

        user_arguments = self.request.arguments
        routers = get_router.get_routers(user_arguments)

        response = {}
        relays, bridges = [], []
        filtered_relays, filtered_bridges, relay_timestamp, bridge_timestamp = routers

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
                3_day_info['first'] = 
                3_day_info['last'] =
                3_day_info['interval'] = 
                3_day_info['factor'] = 
                3_day_info['count'] = 
                3_day_info['values'] = 
                1_week_info['first'] = 
                1_week_info['last'] = 
                1_week_info['interval'] = 
                1_week_info['factor'] = 
                1_week_info['count'] = 
                1_week_info['values'] = 
                1_month_info['first'] = 
                1_month_info['last'] = 
                1_month_info['interval'] = 
                1_month_info['factor'] = 
                1_month_info['count'] = 
                1_month_info['values'] = 
                3_months_info['first'] = 
                3_months_info['last'] = 
                3_months_info['interval'] = 
                3_months_info['factor'] = 
                3_months_info['count'] = 
                3_months_info['values'] = 
                1_year_info['first'] = 
                1_year_info['last'] = 
                1_year_info['interval'] = 
                1_year_info['factor'] = 
                1_year_info['count'] = 
                1_year_info['values'] = 
                5_years_info['first'] = 
                5_years_info['last'] = 
                5_years_info['interval'] = 
                5_years_info['factor'] = 
                5_years_info['count'] = 
                5_years_info['values'] = 
                write_history_info['3 days'] = 3_day_info
                write_history_info['1 week'] = 1_week_info
                write_history_info['1 month'] = 1_month_info
                write_history_info['3 months'] = 3_months_info
                write_history_info['1 year'] = 1_year_info
                write_history_info['5 years'] = 5_years_info
                relay_info['write_history'] = 
