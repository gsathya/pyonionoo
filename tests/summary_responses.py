# List of responses from Pyonionoo

BAD_REQUEST = """<html><title>400: Bad Request</title><body>400: Bad Request</body></html>"""

FULL_SUMMARY = """{"relays_published": "2012-07-03 07:00:00", "bridges_published": "2012-07-02 22:37:06", "relays": [{"n": "sumkledi", "r": true, "f": "0013D22389CD50D0B784A3E4061CB31E8CE8CEB5"}, {"n": "Unnamed", "r": false, "f": "0036D8A9212508D2C963B4BA965FF33FEF9842EB"}], "bridges": [{"n": "Unnamed", "r": false, "f": "000951A845A3B4772F16DEC805DD0144F2BF7E02"}, {"n": "Unnamed", "r": false, "f": "0014A2055278DB3EB0E59EA701741416AF185558"}]}"""


RELAY_SUMMARY = """{"relays_published": "2012-07-03 07:00:00", "bridges_published": "2012-07-02 22:37:06", "relays": [{"n": "sumkledi", "r": true, "f": "0013D22389CD50D0B784A3E4061CB31E8CE8CEB5"}, {"n": "Unnamed", "r": false, "f": "0036D8A9212508D2C963B4BA965FF33FEF9842EB"}], "bridges": []}"""

BRIDGE_SUMMARY = """{"relays_published": "2012-07-03 07:00:00", "bridges_published": "2012-07-02 22:37:06", "relays": [], "bridges": [{"n": "Unnamed", "r": false, "f": "000951A845A3B4772F16DEC805DD0144F2BF7E02"}, {"n": "Unnamed", "r": false, "f": "0014A2055278DB3EB0E59EA701741416AF185558"}]}"""

RUNNING_TRUE = """{"relays_published": "2012-07-03 07:00:00", "bridges_published": "2012-07-02 22:37:06", "relays": [{"n": "sumkledi", "r": true, "f": "0013D22389CD50D0B784A3E4061CB31E8CE8CEB5"}], "bridges": []}"""

RUNNING_FALSE = """{"relays_published": "2012-07-03 07:00:00", "bridges_published": "2012-07-02 22:37:06", "relays": [{"n": "sumkledi", "r": true, "f": "0013D22389CD50D0B784A3E4061CB31E8CE8CEB5"}, {"n": "Unnamed", "r": false, "f": "0036D8A9212508D2C963B4BA965FF33FEF9842EB"}], "bridges": [{"n": "Unnamed", "r": false, "f": "000951A845A3B4772F16DEC805DD0144F2BF7E02"}, {"n": "Unnamed", "r": false, "f": "0014A2055278DB3EB0E59EA701741416AF185558"}]}"""

LOOKUP_RESULT_HASHED_FINGERPRINT = """{"relays_published": "2012-07-03 07:00:00", "bridges_published": "2012-07-02 22:37:06", "relays": [], "bridges": [{"n": "Unnamed", "r": false, "f": "0014A2055278DB3EB0E59EA701741416AF185558"}]}"""

LOOKUP_RESULT_FINGERPRINT = """{"relays_published": "2012-07-03 07:00:00", "bridges_published": "2012-07-02 22:37:06", "relays": [{"n": "sumkledi", "r": true, "f": "0013D22389CD50D0B784A3E4061CB31E8CE8CEB5"}], "bridges": []}"""

COUNTRY_RESULT = """{"relays_published": "2012-07-03 07:00:00", "bridges_published": "2012-07-02 22:37:06", "relays": [{"n": "sumkledi", "r": true, "f": "0013D22389CD50D0B784A3E4061CB31E8CE8CEB5"}, {"n": "Unnamed", "r": false, "f": "0036D8A9212508D2C963B4BA965FF33FEF9842EB"}], "bridges": []}"""

OFFSET_RESULT="""{"relays_published": "2012-07-03 07:00:00", "bridges_published": "2012-07-02 22:37:06", "relays": [], "bridges": [{"n": "Unnamed", "r": false, "f": "000951A845A3B4772F16DEC805DD0144F2BF7E02"}, {"n": "Unnamed", "r": false, "f": "0014A2055278DB3EB0E59EA701741416AF185558"}]}"""

LIMIT_RESULT="""{"relays_published": "2012-07-03 07:00:00", "bridges_published": "2012-07-02 22:37:06", "relays": [{"n": "sumkledi", "r": true, "f": "0013D22389CD50D0B784A3E4061CB31E8CE8CEB5"}, {"n": "Unnamed", "r": false, "f": "0036D8A9212508D2C963B4BA965FF33FEF9842EB"}], "bridges": []}"""

LIMIT_OFFSET_RESULT="""{"relays_published": "2012-07-03 07:00:00", "bridges_published": "2012-07-02 22:37:06", "relays": [{"n": "Unnamed", "r": false, "f": "0036D8A9212508D2C963B4BA965FF33FEF9842EB"}], "bridges": [{"n": "Unnamed", "r": false, "f": "000951A845A3B4772F16DEC805DD0144F2BF7E02"}]}"""
