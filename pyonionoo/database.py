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
    #---------------------------------------------------------------------------------    
    conn = sqlite3.connect('summary.db')
    CURSOR = conn.cursor()
    CURSOR.execute('DROP TABLE IF EXISTS summary')
    CURSOR.execute('CREATE TABLE summary(id INTEGER PRIMARY KEY, type CHARACTER, nickname STRING, fingerprint STRING, running BOOLEAN, time_published STRING, OR_port STRING, dir_port STRING, consensus_weight STRING, country_code STRING, hostname STRING, time_lookup STRING)')

    CURSOR.execute('DROP TABLE IF EXISTS addresses')
    CURSOR.execute('CREATE TABLE addresses(id_of_row INTEGER, address STRING)')
    
    CURSOR.execute('DROP TABLE IF EXISTS flags')
    CURSOR.execute('CREATE TABLE flags(id_of_row INTEGER, flag STRING)')

    with open(SUMMARY) as f:
        router_tuples = []
        for line in f.readlines():
            router = Router(line)
            logging.debug('Adding {} to database.'.format(router.nickname))
            
            if router.is_relay:
                router_type = 'r'
            elif not router.is_relay:
                router_type = 'b'
            
            router_tuples = (router_type, router.nickname, router.fingerprint, router.is_running, router.time_published, router.orport, router.dirport, router.consensus_weight, router.country_code, router.hostname, router.time_of_lookup)

            CURSOR.execute("INSERT INTO summary ('type', 'nickname', 'fingerprint', 'running', 'time_published', 'OR_port', 'dir_port', 'consensus_weight', 'country_code', 'hostname', 'time_lookup') VALUES (?,?,?,?,?,?,?,?,?,?,?)", router_tuples)
            id_num = CURSOR.lastrowid

            address_info = (id_num, router.address)
            CURSOR.execute('INSERT INTO addresses (id_of_row, address) VALUES (?,?)', address_info)

            flags = router.flags
            for flag in flags:
                flag_info = (id_num, flag)
                CURSOR.execute('INSERT INTO flags (id_of_row, flag) VALUES (?,?)', flag_info)
            
    #--------------------------------------------------------------------------------

        conn.commit()

    logging.info('Finished creating database.')

def get_summary_routers(arguments):
    
    summary_database = database()

    routers = []
    return_relays, return_bridges = True, True
    hex_fingerprint, running_filter = None, None
    return_type, return_country, return_search = False, False, False
    asc_cw, desc_cw = False, False
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
            if key == "order":
                for value in values:
                    if value == "consensus_weight":
                        asc_cw = True
                    elif value == "-consensus_weight":
                        desc_cw = True

    filtered_relays, filtered_bridges = [], []
    for row in CURSOR.execute('SELECT type, nickname, fingerprint, running, country_code, time_published, consensus_weight FROM summary'):
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
            for address_row in CURSOR.execute('SELECT address FROM addresses'):
                if search_input in str(address_row[0]):
                    dest.append(row)
        else:
            dest.append(row)

        current_router = datetime.datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S")
        if row[0] == 'r':
            if current_router > relay_timestamp:
                relay_timestamp = current_router
        if row[0] == 'b':
            if current_router > bridge_timestamp:
                bridge_timestamp = current_router

    if asc_cw:
        filtered_relays = sorted(filtered_relays, key=lambda row: row[6])
        filtered_bridges = sorted(filtered_bridges, key=lambda row: row[6])
    elif desc_cw:
        filtered_relays = sorted(filtered_relays, key=lambda row: row[6], reverse=True)
        filtered_bridges = sorted(filtered_bridges, key=lambda row: row[6], reverse=True)

    total_routers = (filtered_relays, filtered_bridges, relay_timestamp, bridge_timestamp)
    return total_routers

