"""
Handle URL request parameters.  Provides the following functions:

parse:  given a GET request parameter dictionary, return a keyword
        argument dictionary suitable for use by the database module
        functions.
"""

import cyclone.web

# Request parameters.
ARGUMENTS = ['type', 'running', 'search', 'lookup', 'country', 'order', 'offset', 'limit']

def parse(arguments):
    """
    @type arguments: dict of string -> list of string.
    @param arguments:  dictionary mapping GET request parameters to valuse.

    @rtype: dict
    @return: dictionary suitable for use for keyword arguments for
        database module functions.
    """

    # These variables will be assigned non-None values if there is a
    # corresponding request parameter (i.e., None means that the corresponding
    # request parameter is not present at all).
    running_filter = None
    type_filter = None
    hex_fingerprint_filter = None
    country_filter = None

    # TODO:  Handle 'search' parameter.
    search_filter = None

    # Ordering offset and limit.
    order_field = None
    order_asc = True
    offset_value = None
    limit_value = None

    # Parse request arguments.
    # TODO:  If a user submits a request with, e.g., two values for running
    # (a boolean flag), what should we do?  Right now we just use the first
    # argument.
    for key, values in arguments.iteritems():
        if key in ARGUMENTS:
            if key == "running":
                value = values[0]
                if value.lower() == 'true':
                    running_filter = True
                elif value.lower() == 'false':
                    running_filter = False
                else:
                    error_msg = 'Invalid argument to running parameter: %s' % value
                    raise cyclone.web.HTTPError(400, error_msg)

            if key == "type":
                value = values[0]
                if value == 'relay':
                    type_filter = 'r'
                elif value == 'bridge':
                    type_filter = 'b'
                else:
                    error_msg = 'Invalid argument to type parameter: %s' % value
                    raise cyclone.web.HTTPError(400, error_msg)

            if key == "lookup":
                hex_fingerprint_filter = values[0]

            if key == "country":
                country_filter = values[0]

            if key == "search":
                search_filter = values[0].split()

            # TODO:  Handle list of ordering fields.
            if key == "order":
                value = values[0]
                order_asc = (value[0] != '-')
                if value[0] == '-':
                    value = value[1:]
                if value == "consensus_weight":
                    order_field = 'consensus_weight'
                else:
                    error_msg = 'Invalid order argument: %s' % value
                    raise cyclone.web.HTTPError(400, error_msg)

            if key == 'offset':
                value = values[0]
                try:
                    offset_value = int(value)
                except ValueError:
                    error_msg = 'Invalid offset argument: %s' % value
                    raise cyclone.web.HTTPError(400, error_msg)

            if key == 'limit':
                value = values[0]
                try:
                    limit_value = int(value)
                except ValueError:
                    error_msg = 'Invalid limit argument: %s' % value
                    raise cyclone.web.HTTPError(400, error_msg)

        else:   # key not in ARGUMENTS
            error_msg = 'Invalid request parameter: %s' % value
            raise cyclone.web.HTTPError(400, error_msg)

    # There must be a better way to do this...
    return {
        'running_filter' : running_filter,
        'type_filter' : type_filter,
        'hex_fingerprint_filter' : hex_fingerprint_filter,
        'country_filter' : country_filter,
        'search_filter' : search_filter,
        'order_field' : order_field,
        'order_asc' : order_asc,
        'offset_value' : offset_value,
        'limit_value' : limit_value
    }
