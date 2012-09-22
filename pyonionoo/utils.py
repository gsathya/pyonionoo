import re

import cyclone.escape
import cyclone.sqlite
import cyclone.web

from twisted.enterprise import adbapi

def is_valid_ip_address(address):
    """
    Checks if a string is a valid IPv4 address.

    :param str address: string to be checked

    :returns: True if input is a valid IPv4 address, False otherwise
    """

    if not isinstance(address, str): return False

    # checks if theres four period separated values
    if address.count(".") != 3: return False

    # checks that each value in the octet are decimal values between 0-255
    for entry in address.split("."):
        if not entry.isdigit() or int(entry) < 0 or int(entry) > 255:
            return False
        elif entry[0] == "0" and len(entry) > 1:
            return False # leading zeros, for instance in "1.2.3.001"

    return True

def is_valid_ipv6_address(address, allow_brackets=False):
    """
    Checks if a string is a valid IPv6 address.

    :param str address: string to be checked
    :param bool allow_brackets: ignore brackets which form '[address]'

    :returns: True if input is a valid IPv6 address, False otherwise
    """

    if allow_brackets:
        if address.startswith("[") and address.endswith("]"):
            address = address[1:-1]

    # addresses are made up of eight colon separated groups of four hex digits
    # with leading zeros being optional
    # https://en.wikipedia.org/wiki/IPv6#Address_format

    colon_count = address.count(":")

    if colon_count > 7:
        return False # too many groups
    elif colon_count != 7 and not "::" in address:
        return False # not enough groups and none are collapsed
    elif address.count("::") > 1 or ":::" in address:
        return False # multiple groupings of zeros can't be collapsed

    for entry in address.split(":"):
        if not re.match("^[0-9a-fA-f]{0,4}$", entry):
            return False

    return True

def is_valid_fingerprint(entry, check_prefix=False):
    """
    Checks if a string is a properly formatted relay fingerprint. This checks for
    a '$' prefix if check_prefix is true, otherwise this only validates the hex
    digits.

    :param str entry: string to be checked
    :param bool check_prefix: checks for a '$' prefix

    :returns: True if the string could be a relay fingerprint, False otherwise.
    """
    hex_digit = "[0-9a-fA-F]"
    fingerprint_pattern = re.compile("^%s{1,40}$" % hex_digit)

    if check_prefix:
        if not entry or entry[0] != "$": return False
        entry = entry[1:]

    return bool(fingerprint_pattern.match(entry))

def is_valid_nickname(entry):
    """
    Checks if a string is a valid format for being a nickname.

    :param str entry: string to be checked

    :returns: True if the string could be a nickname, False otherwise.
    """

    nickname_pattern = re.compile("^[a-zA-Z0-9]{1,19}$")
    return bool(nickname_pattern.match(entry))

class DatabaseMixin(object):
    sqlite = None

    @classmethod
    def setup(self, settings):
        conf = settings.get("sqlite_settings")
        if conf:
            DatabaseMixin.sqlite = cyclone.sqlite.InlineSQLite(conf.database)
