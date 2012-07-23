import pygeoip
import threading
import socket
import router
import util
import stem
import StringIO

from util import Worker, ThreadPool
from router import Router
from stem.descriptor.server_descriptor import RelayDescriptor, BridgeDescriptor


KEYS = ['r', 's', 'v', 'w','p', 'm']
RDNS_LOOKUP_TIMEOUT = 5
RDNS_LOOKUP_WORKERS_NUM = 5

#Move to a different file?
def parse_consensus(raw_contents):
    gi_db = pygeoip.GeoIP('GeoIPCity.dat')
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
    except socket.herror:
        return

def update_router(router, desc):    
    router.version = float(desc.get_annotation_lines()[0].split()[2])
    router.published = desc.published
    router.fingerprint = desc.fingerprint
    router.family = desc.family
    router.platform = desc.platform
    router.exit_policy = desc.exit_policy
    router.contact = desc.contact
    router.advertised_bandwidth = min(desc.average_bandwidth, desc.burst_bandwidth, desc.observed_bandwidth)

def run():
    with open('/Users/sathya/Documents/pyonionoo/data/relay-descriptors/consensuses/2012-07-15-09-00-00-consensus') as f:
        routers = parse_consensus(f.read())
        
    pool = ThreadPool(RDNS_LOOKUP_WORKERS_NUM)
    
    for router in routers.itervalues():
        pool.add_task(get_hostname, router)
    
    for router in routers.itervalues():
        with open('/Users/sathya/Documents/pyonionoo/data/relay-descriptors/server-descriptors/'+router.hex_digest) as f:
            data = f.read()
        
        desc_iter = stem.descriptor.server_descriptor.parse_file(StringIO.StringIO(data))
        desc_entries = list(desc_iter)
        desc = desc_entries[0]
        update_router(router, desc)
    
    pool.wait_completion()

if __name__ == '__main__':
    run()
