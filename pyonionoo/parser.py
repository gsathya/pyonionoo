import re
import datetime

from binascii import a2b_hex
from hashlib import sha1

class Router:
    def __init__(self):
        self.nickname = None
        self.fingerprint = None
        self.hex_fingerprint = None
        self.address = None
        self.addresses = None
        self.exit_addresses = None
        self.or_addresses = None
        self.time_published = None
        self.or_port = None
        self.dir_port = None
        self.flags = None
        self.running = False
        self.consensus_weight = None
        self.country_code = None
        self.hostname = None
        self.time_lookup = None
        self.type = None

    def parse(self, raw_content):
        values = raw_content.split(' ')
        if len(values) < 9:
            #raise Exception
            raise ValueError("Invalid router!")
        if values[0] == "r": self.type = "r"
        else: self.type = "b"

        self.nickname = values[1]
        self.fingerprint = values[2]
        self.hex_fingerprint = sha1(a2b_hex(self.fingerprint)).hexdigest()

        if ';' in values[3]: 
            address_parts = values[3].split(';')
            if len(address_parts) < 3:
                #raise Exception
                pass
            self.address = address_parts[0]
            if len(address_parts[1]) > 0:
                self.or_addresses = address_parts[1].split(',')
            if len(address_parts[2]) > 0:
                self.exit_addresses = address_parts[2].split(',')
        else:
            self.address = values[3]
        
        self.time_published = self._parse_timestamp(values[4] + ' ' + values[5])
        
        self.or_port = int(values[6])
        self.dir_port = int(values[7])
        self.flags = values[8].split(',')
        for flag in self.flags:
            if flag == "Running":
                self.running = True
        self.consensus_weight = int(values[9])
        self.country_code = values[10]
        if values[11] != "null" : self.hostname = values[11]
        self.time_lookup = int(values[12])
    
    def _parse_timestamp(self, content):
      """
      Parses a 'YYYY-MM-DD HH:MM:SS' entry.
      """
      
      try:
        timestamp = datetime.datetime.strptime(content, "%Y-%m-%d %H:%M:%S")
        return timestamp
      except ValueError:
        raise ValueError("Timestamp wasn't parseable: %s" % line)

    def get_router_tuple(self, fields):
        """
        Returns a tuple of values.

        @param type: list/tuple
        @param fields: attributes of Router for which the values must be returned

        @rtype: tuple
        @return: list of values corresponding to the fields
        """

        router_list = []
        for field in fields:
            if field == "search":
                value = ' %s %s %s %s' % (self.fingerprint, self.hex_fingerprint,
                                          self.nickname, self.address)
            elif field == "flags":
                value = ' '.join(self.flags)
                # add leading space
                value = ' %s' % value
            else:
                value = getattr(self, field)
            router_list.append(value)

        return tuple(router_list)
