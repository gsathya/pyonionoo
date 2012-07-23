from binascii import b2a_hex, a2b_hex, a2b_base64
import datetime

class Router:
    def __init__(self, as_db = None, gi_db = None):
        self.nick = None
        self.fingerprint = None
        self.address = None
        self.addresses = None
        self.exit_addresses = None
        self.or_addresses = None
        self.time_published = None
        self.dir_port = None
        self.or_port = None
        self.flags = None
        self.consensus_weight = None
        self.hostname = None
        self.time_of_lookup = None
        self.is_relay = None
        self.digest = None
        self.hex_digest = None
        self.as_no = None
        self.as_name = None
        self.country = None
        self.country_name = None
        self.longitude = None
        self.latitude = None
        self.region_name = None #Always none
        self.city = None
        self.is_running = False
        self.as_db = as_db
        self.gi_db = gi_db
        
    def _get_geoip_details(self):
        data = self.gi_db.record_by_addr(self.ip)
        if data:
            self.country = data['country_code']
            self.country_name = data['country_name']
            self.city = data['city']
            self.longitude = data['longitude']
            self.latitude = data['latitude']

    def _get_as_details(self):
        try:
            value = self.as_db.org_by_addr(str(self.ip)).split()
            return value[0], value[1]
        except:
            return None, None
    
    def _parse_timestamp(self, date, time):
      """
      Parses a 'YYYY-MM-DD HH:MM:SS' entry.
      """

      timestamp = date+' '+time
      try:
        timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        return timestamp
      except ValueError:
        raise ValueError("Timestamp wasn't parseable: %s" % timestamp)
    
    def add(self, key, values):
        if key == 'r':
            self.is_relay = True
            self.nick = values[0]
            self.digest = values[2]
            self.hex_digest = b2a_hex(a2b_base64(self.digest+"="))
            self.time_published = self._parse_timestamp(values[3], values[4])
            self.ip = values[5]
            self.or_port = values[6]
            self.dir_port = values[7]
            if self.gi_db:
                self._get_geoip_details()
            if self.as_db:
                self.as_no, self.as_name = self._get_as_details()
        if key == 's':
            self.flags = values
        if key == 'w':
            self.bandwidth = int(values[0].split('=')[1])
