import datetime

from pyonionoo.parser import Router

ARGUMENTS = ['type', 'running', 'search', 'lookup', 'country', 'order', 'offset', 'limit']

def get_routers(arguments):
    
    routers = []
    filtered_relays, filtered_bridges = [], []
    return_relays, return_bridges = True, True
    hex_fingerprint, running_filter = None, None
    return_type, return_country, return_search = False, False, False
    relay_timestamp = datetime.datetime(1900, 1, 1, 1, 0)
    bridge_timestamp = datetime.datetime(1900, 1, 1, 1, 0)
    
    for key, values in arguments.iteritems():
        if key in ARGUMENTS:
            if key == "running":
                for value in values:
                    running_filter = value
            if key == "type":
                return_type = True
                for value in values:
                    if value == "relay":
                        return_bridges = False
                    if value == "bridge":
                        return_relays = False
            if key == "lookup":
                for value in values:
                    hex_fingerprint = value
            if key == "country":
                for value in values:
                    return_country = True
                    country_code = value
            if key == "search":
                for value in values:
                    return_search = True
                    search_input = value
    
    with open('/home/mchang01/HFOSS2012/pyonionoo/pyonionoo/summary') as f:

        for line in f.readlines():
            router = Router(line)
            
            if router.is_relay and return_relays:
                dest = filtered_relays
                time_dest = relay_timestamp
            elif not router.is_relay and return_bridges:
                dest = filtered_bridges
                time_dest = bridge_timestamp
            else:
                continue
            if return_type:
                dest.append(router)
            elif running_filter:
                if router.is_running == eval(running_filter.title()):
                    dest.append(router)
            elif hex_fingerprint:
                if hex_fingerprint == router.fingerprint:
                    dest.append(router)
                    break
            elif return_country:
                if router.country_code == country_code:
                    dest.append(router)
            elif return_search:
                if search_input in router.nickname:
                    dest.append(router)
                if search_input in router.fingerprint:
                    dest.append(router)
                if search_input in router.address:
                    dest.append(router)
            else:
                dest.append(router)
            
            current_router = router.time_published
            if current_router > time_dest:
                time_dest = current_router

        total_routers = (filtered_relays, filtered_bridges,
                         relay_timestamp, bridge_timestamp)
        return total_routers
