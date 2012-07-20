#!/bin/bash

export PYTHONPATH=$PYTHONPATH:`dirname $0`
/usr/bin/env python /usr/bin/twistd -n cyclone -p 8888 -l 0.0.0.0 \
       -r pyonionoo.web.Application -c pyonionoo.conf $*
