import cyclone.escape
import cyclone.redis
import cyclone.sqlite
import cyclone.web

from twisted.enterprise import adbapi

class DatabaseMixin(object):
    mysql = None
    redis = None
    sqlite = None

    @classmethod
    def setup(self, settings):
        conf = settings.get("sqlite_settings")
        if conf:
            DatabaseMixin.sqlite = cyclone.sqlite.InlineSQLite(conf.database)

        conf = settings.get("redis_settings")
        if conf:
            DatabaseMixin.redis = cyclone.redis.lazyConnectionPool(
                            conf.host, conf.port, conf.dbid, conf.poolsize)

        conf = settings.get("mysql_settings")
        if conf:
            DatabaseMixin.mysql = adbapi.ConnectionPool("MySQLdb",
                            host=conf.host, port=conf.port, db=conf.database,
                            user=conf.username, passwd=conf.password,
                            cp_min=1, cp_max=conf.poolsize,
                            cp_reconnect=True, cp_noisy=conf.debug)
