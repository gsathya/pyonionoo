import pygeoip
import threading
import socket
import router
import util
from util import Worker, ThreadPool
from router import Router

KEYS = ['r', 's', 'v', 'w','p', 'm']
RDNS_LOOKUP_TIMEOUT = 5
RDNS_LOOKUP_WORKERS_NUM = 5

#Move to a different file?
def parse_consensus(raw_contents):
    gi_db = pygeoip.GeoIP('GeoIP.dat')
    as_db = pygeoip.GeoIP('GeoIPASNum.dat')

    remaining_lines = raw_contents.split("\n")
    routers = {}
    router = None
    
    for line in remaining_lines:
        # empty line
        if not line: continue
        key = line.split()[0]
        values = line.split()[1:]
        
        if key == 'r':
            if router:
                routers[router.hex_digest] = router
            router = Router(as_db, gi_db)
            router.add(key, values)
        elif key in KEYS:
            router.add(key, values)
    
    return routers

def get_hostname(router):
    try:
        router.hostname = socket.gethostbyaddr(router.ip)[0]
        print router.hostname
    except socket.herror:
        return None, None, None

def run():
    with open('/Users/sathya/Documents/pyonionoo/data/relay-descriptors/consensuses/2012-07-12-10-00-00-consensus') as f:
        routers = parse_consensus(f.read())
        
    pool = ThreadPool(RDNS_LOOKUP_WORKERS_NUM)        
    
    for router in routers.itervalues():
        pool.add_task(get_hostname, router)
        
    pool.wait_completion()

if __name__ == '__main__':
    run()
