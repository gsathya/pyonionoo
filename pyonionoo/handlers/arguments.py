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
    lookup_filter = None
    country_filter = None
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
            value = values[0]
            error_msg = 'Invalid argument to %s parameter: %s' % (key, value)

            if key == "running":
                if value == 'true':
                    running_filter = True
                elif value == 'false':
                    running_filter = False
                else:
                    raise cyclone.web.HTTPError(400, error_msg)

            elif key == "type":
                if value == 'relay':
                    type_filter = 'r'
                elif value == 'bridge':
                    type_filter = 'b'
                else:
                    raise cyclone.web.HTTPError(400, error_msg)

            elif key == "lookup":
                if len(value) == 40:
                    lookup_filter = value
                else:
                    raise cyclone.web.HTTPError(400, error_msg)

            elif key == "country":
                if len(value) == 2:
                    country_filter = value
                else:
                    raise cyclone.web.HTTPError(400, error_msg)

            elif key == "search":
                if value:
                    search_filter = value.split()
                else:
                    raise cyclone.web.HTTPError(400, error_msg)

            # TODO:  Handle list of ordering fields.
            # This is pretty borked.
            elif key == "order":
                value = value.split()
                order_asc = (value[0] != '-')
                if value[0] == '-':
                    value = value[1:]
                if value == "consensus_weight":
                    order_field = 'consensus_weight'
                else:
                    raise cyclone.web.HTTPError(400, error_msg)

            elif key == 'offset':
                try:
                    offset_value = int(value)
                except ValueError:
                    raise cyclone.web.HTTPError(400, error_msg)

            elif key == 'limit':
                try:
                    limit_value = int(value)
                except ValueError:
                    raise cyclone.web.HTTPError(400, error_msg)

        # key not in ARGUMENTS
        else:
            error_msg = 'Invalid request parameter: %s' % value
            raise cyclone.web.HTTPError(400, error_msg)

    # There must be a better way to do this...
    return {
        'running_filter' : running_filter,
        'type_filter' : type_filter,
        'lookup_filter' : lookup_filter,
        'country_filter' : country_filter,
        'search_filter' : search_filter,
        'order_field' : order_field,
        'order_asc' : order_asc,
        'offset_value' : offset_value,
        'limit_value' : limit_value
    }
