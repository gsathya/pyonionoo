import datetime
import sqlite3

import logging
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

from pyonionoo.parser import Router

ARGUMENTS = ['type', 'running', 'search', 'lookup', 'country', 'order', 'offset', 'limit']

SUMMARY = '/home/mchang01/HFOSS2012/pyonionoo/pyonionoo/summary'

CURSOR = None

def database():
    logger.info('Creating database.')
    global CURSOR
    
    conn = sqlite3.connect('summary.db')
    CURSOR = conn.cursor()
    CURSOR.execute('DROP TABLE IF EXISTS summary')
    CURSOR.execute('CREATE TABLE summary(id INTEGER PRIMARY KEY AUTOINCREMENT, type CHARACTER, nickname STRING, fingerprint STRING, running BOOLEAN, time_published STRING, OR_port STRING, dir_port STRING, consensus_weight STRING, country_code STRING, hostname STRING, time_lookup STRING)')
    
    columns = ('type', 'nickname', 'fingerprint', 'running', 'time_published', 'OR_port', 'dir_port', 'consensus_weight', 'country_code', 'hostname', 'time_lookup')
    insert_stmt = 'INSERT INTO summary ({}) VALUES ({})'.format(','.join(columns),
            ','.join(['?']*len(columns)))
    with open(SUMMARY) as f:
        router_tuples = []
        for line in f.readlines():
            router = Router(line)
            logging.debug('Adding {} to database.'.format(router.nickname))
            
            if router.is_relay:
                router_type = 'r'
            elif not router.is_relay:
                router_type = 'b'
            
            router_tuples.append((router_type, router.nickname, router.fingerprint, router.is_running, router.time_published, router.orport, router.dirport, router.consensus_weight, router.country_code, router.hostname, router.time_of_lookup))
        CURSOR.executemany(insert_stmt, router_tuples)
        conn.commit()
        # CURSOR.close()

    logging.info('Finished creating database.')

def get_summary_routers(arguments):
    
    summary_database = database()

    routers = []
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

    filtered_relays, filtered_bridges = [], []
    for row in CURSOR.execute('SELECT type, nickname, fingerprint, running, country_code, time_published FROM summary'):
        if row[0] == 'r' and return_relays:
            dest = filtered_relays
        elif row[0] == 'b' and return_bridges:
            dest = filtered_bridges
        else:
            continue
        if return_type:
            dest.append(row)
        elif running_filter:
            if running_filter.title() == 'True':
                running = True
            elif running_filter.title() == 'False':
                running = False
            else: raise ValueError('A proper boolean value was not provided.')
            if row[3] == running:
                dest.append(row)
        elif hex_fingerprint:
            if hex_fingerprint == row[2]:
                dest.append(row)
                break
        elif return_country:
            if country_code == row[4]:
                dest.append(row)
        elif return_search:
            if search_input in row[1]:
                dest.append(row)
            if search_input in row[2]:
                dest.append(row)
            # ADDRESS SEARCH
        else:
            dest.append(row)

        current_router = datetime.datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S")
        if row[0] == 'r':
            if current_router > relay_timestamp:
                relay_timestamp = current_router
        if row[0] == 'b':
            if current_router > bridge_timestamp:
                bridge_timestamp = current_router

    total_routers = (filtered_relays, filtered_bridges, relay_timestamp, bridge_timestamp)
    return total_routers

