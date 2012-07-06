#!/bin/bash

export PYTHONPATH=`dirname $0`
twistd -n cyclone -p 8888 -l 0.0.0.0 \
       -r pyonionoo.web.Application -c pyonionoo.conf $*
