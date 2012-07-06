import re
import datetime

class Router:
    def __init__(self, raw_content):
        self.nickname = None
        self.fingerprint = None
        self.address = None
        self.addresses = None
        self.exit_addresses = None
        self.or_addresses = None
        self.time_published = None
        self.orport = None
        self.dirport = None
        self.flags = None
        self.consensus_weight = None
        self.country_code = None
        self.hostname = None
        self.time_of_lookup = None
        self.is_relay = None
        self._parse(raw_content)

    def _parse(self, raw_content):
        values = raw_content.split()
        if len(values) < 9:
            #raise Exception
            pass
        if values[0] == "r":
            self.is_relay = True
        self.nickname = values[1]
        self.fingerprint = values[2]

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
        
        self.orport = int(values[6])
        self.dirport = int(values[7])
        self.flags = values[8].split(',')
        self.consensus_weight = values[9]
        self.country_code = values[10]
        if values[11] != "null" : self.hostname = values[11]
        self.time_of_lookup = int(values[12])

    def _parse_timestamp(self, content):
      """
      Parses a 'YYYY-MM-DD HH:MM:SS' entry.
      """
      
      try:
        timestamp = datetime.datetime.strptime(content, "%Y-%m-%d %H:%M:%S")
        return timestamp
      except ValueError:
        raise ValueError("Timestamp wasn't parseable: %s" % line)
