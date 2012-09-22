"""
Handle URL request parameters.  Provides the following functions:

    parse:  given a GET request parameter dictionary, return a keyword
        argument dictionary suitable for use by the database module
        functions.
"""

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
                    raise ValueError(
                        'Invalid argument to running parameter: {}.'.format(
                            value))
            if key == "type":
                value = values[0]
                if value == 'relay':
                    type_filter = 'r'
                elif value == 'bridge':
                    type_filter = 'b'
                else:
                    raise ValueError(
                        'Invalid argument to type parameter: {}.'.format(
                            value))
            if key == "lookup":
                hex_fingerprint_filter = values[0]
            if key == "country":
                country_filter = values[0]

            # XXX: The protocol allows a list of search terms.  In a URL-based
            # GET request, these would appear as search=term1&search=term2...,
            # and then values would be [term1, term2,...].  But the protocol
            # specifies that multiple terms appear as a single argument for
            # the search parameter, which is then given to us as a single
            # (space-separated) string.
            if key == "search":
                search_filter = values[0]

            # TODO:  Handle list of ordering fields.
            if key == "order":
                value = values[0]
                order_asc = (value[0] != '-')
                if value[0] == '-':
                    value = value[1:]
                if value == "consensus_weight":
                    order_field = 'consensus_weight'
                else:
                    raise ValueError('Invalid order argument: {}'.format(value))

            if key == 'offset':
                value = values[0]
                try:
                    offset_value = int(value)
                except ValueError:
                    raise ValueError('Invalid offset argument: {}'.format(value))

            if key == 'limit':
                value = values[0]
                try:
                    limit_value = int(value)
                except ValueError:
                    raise ValueError('Invalid limit argument: {}'.format(value))

        else:   # key not in ARGUMENTS
            raise NotImplementedError('Invalid request parameter: {}'.format(key))

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

