import datetime
import sqlite3

from pyonionoo.parser import Router

# Summary document that will be read into an SQLite database.  This should
# probably be defined in a configuration file somewhere.
SUMMARY = 'summary'

# Database schemas.
# Summary database:  in conjunction with addresses and flags, holds the
# information in the summary document.  addresses and flags are lists of
# IP addresses and flags, respectively.  In order to support searching
# by these entries, we put them in separate tables, linked by id.
# Note that as per the SQLite documentation, the id field of summary_schema
# will be made into an alias for rowid.
summary_tbl_name = 'summary'
summary_schema = """
id INTEGER PRIMARY KEY, 
type CHARACTER, 
nickname STRING, 
fingerprint STRING, 
running BOOLEAN, 
time_published STRING, 
OR_port STRING, 
dir_port STRING, 
consensus_weight INTEGER, 
country_code STRING, 
hostname STRING, 
time_lookup STRING
"""

addresses_tbl_name = 'addresses'
addresses_schema = """
id_of_row INTEGER, 
address STRING
"""

flags_tbl_name = 'flags'
flags_schema = """
id_of_row INTEGER, 
flag STRING
"""

def _create_table(conn, tbl_name, schema):
    """
    Create a database table; drop a table by the same name if it already
    exists.

    @type conn: sqlite3.Connector
    @param conn:  open database connection.

    @type tbl_name: string
    @param tbl_name: the name of the database table.

    @type schema: string
    @param schema: the SQLite schema for the table.
    """

    cursor = conn.cursor()

    # Can only use placeholders in select statements?
    cursor.execute('DROP TABLE IF EXISTS {}'.format(tbl_name))
    cursor.execute('CREATE TABLE {} ({})'.format(tbl_name, schema))

    conn.commit()

    return

def database():
    """
    Create the database.

    rtype: sqlite3.Connection
    return:  A connection object for the database that has been created.

    TODO:  Make this a single atomic transaction.
    """

    conn = sqlite3.connect('summary.db')

    # We will need name-based access to the rows.
    conn.row_factory = sqlite3.Row

    # Create the tables.
    _create_table(conn, summary_tbl_name, summary_schema)
    _create_table(conn, flags_tbl_name, flags_schema)
    _create_table(conn, addresses_tbl_name, addresses_schema)

    # Create the summary database.  We could accumulate all the router tuples
    # and then insert them with an executemany(...) in one go, except that
    # makes it more time consuming to create the flags and addresses tables.
    # In effect, to create those tables, we would have to query summary
    # for each relay fingerprint in order to get the id of the row in
    # summary for that fingerprint, in order to set the corresopnding id
    # field in the flags/addresses table.  Here we can avoid all those
    # selects, because the rowid attribute of the cursor is set to that
    # id field right after we execute the (individual) insert statements.
    with open(SUMMARY) as f:
        CURSOR = conn.cursor()

        for line in f.readlines():
            router = Router(line)
            
            router_type = 'r' if router.is_relay else 'b'
            
            # parser.Router.consensus_weight is a string???
            router_tuple = (router_type, router.nickname, router.fingerprint, router.is_running, router.time_published, router.orport, router.dirport, int(router.consensus_weight), router.country_code, router.hostname, router.time_of_lookup)

            # TODO: Determine whether sqlite3 optimizes by remembering
            # this insert command and not parsing it every time it sees
            # it.  This is mentioned in PEP 249, but we aren't sure where
            # the PEP says that implementations might optimize in this way,
            # or might allow users to optimize in this way.
            CURSOR.execute("INSERT INTO summary ('type', 'nickname', 'fingerprint', 'running', 'time_published', 'OR_port', 'dir_port', 'consensus_weight', 'country_code', 'hostname', 'time_lookup') VALUES (?,?,?,?,?,?,?,?,?,?,?)", router_tuple)
            id_num = CURSOR.lastrowid

            address_info = (id_num, router.address)
            CURSOR.execute('INSERT INTO addresses (id_of_row, address) VALUES (?,?)', address_info)

            flags = router.flags
            for flag in flags:
                flag_info = (id_num, flag)
                CURSOR.execute('INSERT INTO flags (id_of_row, flag) VALUES (?,?)', flag_info)
            
    #--------------------------------------------------------------------------------

        conn.commit()

    return conn

def get_summary_routers(
        running_filter=None, type_filter=None, hex_fingerprint_filter=None,
        country_filter=None, search_filter=None,
        order_field=None, order_asc=True, offset_value=None, limit_value=None):
    """
    Get summary document according to request parameters.

    @rtype: tuple.
    @return: tuple of form (relays, bridges, relays_time, bridges_time), where
        * relays (bridges) is a list of sqlite3.Row, each of which consists of the
          various attributes.  The important part is that each element of
          relays (bridges) can be treated as a dictionary, with keys
          the same as the database fields.
        * relays_time (bridges_time) is a datetime object with the most
          recent timestamp of the relay descriptors in relays.
    """
    
    conn = database()

    # Timestamps of most recent relay/bridge in the returned set.
    relay_timestamp = datetime.datetime(1900, 1, 1, 1, 0)
    bridge_timestamp = datetime.datetime(1900, 1, 1, 1, 0)

    # Build up a WHERE clause based on the request parameters.  We only
    # consider the case in which the client specifies 'search' or
    # some subset (possibly empty) of {'running', 'type', 'lookup', 'country'}.
    clauses = []
    if search_filter:
        # We have to do some heuristics here, because the search filters
        # do not come with anything to identify which field they correspond
        # to.  E.g., the request search=ffa means any relay with nickname
        # starting with 'ffa' or fingerprint starting with 'ffa' or '$ffa'.

        # Actually, this is a moderately painful parameter to implement.
        # Testing for an IP address probably means using regular expressions.
        # SQLite doesn't suppor them without a user-defined function.  
        # Matching against a Python RE is easy to do, but then we have
        # to have a where clause that matches against the beginning of a
        # field value, and SQLite doesn't appear to support such a search
        # (unless, of course, you want to write a user-defined match()
        # function).

        pass
    else:
        if running_filter != None:
            clauses.append("running = {}".format(int(running_filter)))
        if type_filter != None:
            clauses.append("type = '{}'".format(type_filter))
        if hex_fingerprint_filter != None:
            clauses.append("fingerprint = '{}'".format(hex_fingerprint_filter))
        if country_filter != None:
            clauses.append("country = '{}'".format(country_filter))
    where_clause = 'WHERE {}'.format(' and '.join(clauses)) if clauses else ''

    # Construct the ORDER, LIMIT, and OFFSET clauses.
    order_clause = ''
    if order_field != None:
        order_clause = 'ORDER BY {} {}'.format(order_field, 
                'ASC' if order_asc else 'DESC')
    limit_clause = ''
    if limit_value != None:
        limit_clause = 'LIMIT {}'.format(limit_value)
    offset_clause = ''
    if offset_value != None:
        offset_clause = 'OFFSET {}'.format(offset_value)

    filtered_relays, filtered_bridges = [], []
    cursor = conn.cursor()
    for row in cursor.execute('SELECT type, nickname, fingerprint, running, country_code, time_published, consensus_weight FROM summary {} {} {} {}'.format(where_clause, order_clause, limit_clause, offset_clause)):

        # Set the destination list for this router.
        dest = filtered_relays if row[0] == 'r' else filtered_bridges
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

