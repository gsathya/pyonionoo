import datetime
import logging
import os
import sqlite3
import threading
import time

from pyonionoo.parser import Router

# Name of the SQLite database.  This should be defined in a configuration file
# somewhere.  And it should be ':memory:', not a file.  BUT:  it seems that
# (1) sqlite3.Connection objects are not thread-safe, and (2) if different
# threads connect() to ':memory:', they each get their own in-memory database.
# We don't know how to fix this yet, but it must be possible.
# Thread-safety is relevant here, because each request should be handled
# in its own thread so the application doesn't block while processing
# a single request.  Asynchronous handlers (a la twisted and cyclone) don't
# really seem to do the job, because we cannot incrementally return
# a JSON object; we need all of the data in order to construct the
# JSON object, and so these requests are inherently synchronous.
DBNAME = 'summary.db'

# Time at which we created the sqlite database from the summary file.
DB_CREATION_TIME = -1

# Interval (in seconds) that we check to update the database.  See
# freshen_database().
DB_UPDATE_INTERVAL = 60

# The timer object used for updating the database.
FRESHEN_TIMER = None

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
type TEXT,
nickname TEXT,
fingerprint TEXT collate NOCASE,
hashed_fingerprint TEXT collate NOCASE,
running BOOLEAN,
time_published TEXT,
or_port TEXT,
dir_port TEXT,
consensus_weight INTEGER,
country_code TEXT collate NOCASE,
hostname TEXT,
time_lookup TEXT,
flags TEXT,
addresses TEXT,
search TEXT collate NOCASE
"""

def _create_table(conn, tbl_name, schema):
    """
    Create a database table; drop a table by the same name if it already
    exists.  This function does not commit the table creation instructions.

    @type conn: sqlite3.Connector
    @param conn:  open database connection.

    @type tbl_name: string
    @param tbl_name: the name of the database table.

    @type schema: string
    @param schema: the SQLite schema for the table.
    """

    cursor = conn.cursor()

    logging.info("Creating table %s" % (tbl_name))
    # Can only use placeholders in select statements?
    cursor.execute('DROP TABLE IF EXISTS %s' % tbl_name)
    cursor.execute('CREATE TABLE %s (%s)' % (tbl_name, schema))
    logging.info("Created table %s" % (tbl_name))

def bootstrap_database(metrics_out, summary_file):
    """
    Bootstraps the database creation process:
      * Create 3 databases - summary, flags, addresses
      * Updates the databases

    @type metrics_out: string
    @param metrics_out: path to metrics data dir

    @type summary_file: string
    @param summary_file: summary file name
    """

    summary_file = os.path.join(metrics_out, summary_file)

    conn = get_database_conn()

    # Create the tables.
    _create_table(conn, summary_tbl_name, summary_schema)

    conn.commit()

    update_databases(summary_file)

def update_databases(summary_file=None):
    """
    Updates the database.

    This operation operates as a single transaction.  Therefore,
    the database can be read by other requests while it is being
    performed, and those reads will correspond to the "un-updated"
    database.  Once this function completes, all future reads will be
    from the "updated" database.

    @type summary_file: string
    @param summary_file: full path to the summary file
    """
    global DB_CREATION_TIME

    if DB_CREATION_TIME >= os.stat(summary_file).st_mtime:
        return

    logging.info("Updating database")

    # It seems that the default isolation_level is probably OK for
    # all of this to be done in a single transaction.
    conn = get_database_conn()

    # First delete all records.
    logging.info("Deleting data from databases")
    CURSOR = conn.cursor()
    CURSOR.execute('DELETE FROM %s' % summary_tbl_name)

    # Create the summary database.  We could accumulate all the router tuples
    # and then insert them with an executemany(...) in one go, except that
    # makes it more time consuming to create the flags and addresses tables.
    # In effect, to create those tables, we would have to query summary
    # for each relay fingerprint in order to get the id of the row in
    # summary for that fingerprint, in order to set the corresopnding id
    # field in the flags/addresses table.  Here we can avoid all those
    # selects, because the rowid attribute of the cursor is set to that
    # id field right after we execute the (individual) insert statements.
    summary_fields = ('type', 'nickname', 'fingerprint', 'hashed_fingerprint', 'running',
                      'time_published', 'or_port', 'dir_port', 'consensus_weight',
                      'country_code', 'hostname', 'time_lookup', 'flags', 'addresses', 'search')

    insert_stmt = 'insert into %s (%s) values (%s)'

    # create insertion statement for summary table
    summary_insert_stmt = (insert_stmt % (summary_tbl_name, ','.join(summary_fields),
                                          ','.join(['?']*len(summary_fields))))

    if not summary_file:
        # raise Exception?
        return

    with open(summary_file) as f:
        for line in f.readlines():
            router = Router()
            router.parse(line)

            router_tuple = router.get_router_tuple(summary_fields)

            # TODO: Determine whether sqlite3 optimizes by remembering
            # this insert command and not parsing it every time it sees
            # it.  This is mentioned in PEP 249, but we aren't sure where
            # the PEP says that implementations might optimize in this way,
            # or might allow users to optimize in this way.
            CURSOR.execute(summary_insert_stmt, router_tuple)
            id_num = CURSOR.lastrowid

    conn.commit()
    logging.info("Table updated")
    DB_CREATION_TIME = time.time()

    FRESHEN_TIMER = threading.Timer(DB_UPDATE_INTERVAL, update_databases, summary_file)
    FRESHEN_TIMER.start()

def cancel_freshen():
    FRESHEN_TIMER.cancel()

def get_database_conn():
    conn = sqlite3.connect(DBNAME)
    return conn

def query_summary_tbl(running_filter=None, type_filter=None, hex_fingerprint_filter=None,
                      country_filter=None, search_filter=None, order_field=None,
                      order_asc=True, offset_value=None, limit_value=None,
                      fields=('fingerprint',)):
    conn = get_database_conn()
    cursor = conn.cursor()
    # Build up a WHERE clause based on the request parameters.  We only
    # consider the case in which the client specifies 'search' or
    # some subset (possibly empty) of {'running', 'type', 'lookup', 'country'}.
    clauses = []
    if search_filter:
        for search_string in search_filter:
            if search_string[0] == '$':
                search_string = ''.join(search_string[1:])
            clauses.append("search like '%% %s%%'" % search_string)
    if running_filter:
        clauses.append("running = %s" % int(running_filter))
    if type_filter:
        clauses.append("type = '%s'" % type_filter)
    if hex_fingerprint_filter:
        clauses.append("fingerprint = '%s' or hashed_fingerprint = '%s'" %
                       (hex_fingerprint_filter, hex_fingerprint_filter))
    if country_filter:
        clauses.append("country_code = '%s'" % country_filter)
    where_clause = ('WHERE %s' % ' and '.join(clauses)) if clauses else ''

    # Construct the ORDER, LIMIT, and OFFSET clauses.
    order_clause = ''
    if order_field:
        order_clause = 'ORDER BY %s %s' % (order_field,
                                           'ASC' if order_asc else 'DESC')
    limit_clause = ''
    if limit_value:
        limit_clause = 'LIMIT %s' % limit_value
    offset_clause = ''
    if offset_value:
        if not limit_value:
            # sqlite doesn't support OFFSET without a LIMIT clause, this is
            # a hack to get around that.
            limit_clause = 'LIMIT -1'
        offset_clause = 'OFFSET %s' % offset_value
    cursor.execute('SELECT %s FROM summary %s %s %s %s' %
                   (','.join(fields), where_clause, order_clause, limit_clause,
                    offset_clause))

    return cursor.fetchall()

def get_timestamp():
    """
    Get the latest known published timestamp of relay consensus and network
    consensus document

    @rtype: tuple
    @return: (relay_timestamp, bridge_timestamp) where
             relays_timestamp, bridges_timestamp is a datetime object
    """

    relay_timestamp, bridge_timestamp = None, None
    conn = get_database_conn()
    cursor = conn.cursor()

    cursor.execute('SELECT MAX(time_published) FROM summary WHERE type="r"')
    relay_timestamp = datetime.datetime.strptime(cursor.fetchone()[0], "%Y-%m-%d %H:%M:%S")

    cursor.execute('SELECT MAX(time_published) FROM summary WHERE type="b"')
    bridge_timestamp = datetime.datetime.strptime(cursor.fetchone()[0], "%Y-%m-%d %H:%M:%S")

    return (relay_timestamp, bridge_timestamp)

def get_summary_routers(running_filter=None, type_filter=None, hex_fingerprint_filter=None,
                        country_filter=None, search_filter=None, order_field=None,
                        order_asc=True, offset_value=None, limit_value=None):
    """
    Get summary document according to request parameters.

    @rtype: tuple.
    @return: tuple of form (relays, bridges, relays_time, bridges_time), where
             * relays/bridges is a list of Router objects
             * relays_timestamp/bridges_timestamp is a datetime object with the most
               recent timestamp of the relay/bridges descriptors in relays.
    """

    relay_timestamp, bridge_timestamp = get_timestamp()

    relays, bridges = [], []
    fields = ('type', 'nickname', 'fingerprint', 'running', 'country_code',
            'time_published', 'consensus_weight')
    for row in query_summary_tbl(running_filter, type_filter, hex_fingerprint_filter,
                                 country_filter, search_filter,order_field, order_asc,
                                 offset_value, limit_value, fields):
        router = Router()

        # This is magic
        map(lambda (attr, value): setattr(router, attr, value), zip(fields, row))

        if row[0] == 'r': relays.append(router)
        if row[0] == 'b': bridges.append(router)

    total_routers = (relays, bridges, relay_timestamp, bridge_timestamp)
    return total_routers
