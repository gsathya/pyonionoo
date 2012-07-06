=====================
Pyonionoo
=====================
:Info: This is the source code of pyonionoo

About
=====

This file has been created automatically by cyclone-tool for pyonionoo.
It contains the following files:

- ``start.sh``: simple shell script to start the server
- ``pyonionoo.conf``: configuration file for the web server
- ``pyonionoo/__init__.py``: information such as author and version of this package
- ``pyonionoo/web.py``: map of url handlers and main class of the web server
- ``pyonionoo/config.py``: configuration parser for ``pyonionoo.conf``
- ``pyonionoo/views.py``: code of url handlers for the web server
- ``scripts/debian-init.d``: generic debian start/stop init script
- ``scripts/debian-multicore-init.d``: run one instance per core on debian
- ``scripts/localefix.py``: script to fix html text before running ``xgettext``
- ``scripts/cookie_secret.py``: script for generating new secret key for the web server

Running
-------

For development and testing::

    twistd -n cyclone --help
    twistd -n cyclone -r pyonionoo.web.Application [--help]

For production::

    twistd cyclone \
    	   --logfile=/var/log/pyonionoo.log \
    	   --pidfile=/var/run/pyonionoo.pid \
	   -r pyonionoo.web.Application

