import json

def has_fp(relay_fp, data, relay=True):
    """
    relay_fp - fingerprint of relay
    data - JSON object
    relay - relay or bridge
    """

    if relay: relay_type = "relays"
    else: relay_type = "bridges"
    
    for relay in data[relay_type]:
        if relay_fp in relay.values(): return True

    return False

def number_of_relays(data):
    """
    data - JSON object
    """

    return len(data['relays'])

def number_of_bridges(data):
    """
    data - JSON object
    """

    return len(data['bridges'])

def check_flag(relay, flag):
    """
    relay - relay info
    flag - flag to check
    """

    if flag in relay['flags']: return True
    return False

def contains_required_fields(data):
    """
    relays_published, bridges_published, relays, bridges
    are required fields.
    """

    required_fields = set(["relays_published", "bridges_published",
                       "relays", "bridges"])

    if set(data.keys()) == required_fields:
        return True
    return False
