# -*- coding:utf-8 -*-


from tornado.options import options

# ping db periodically to avoid mysql go away
#PeriodicCallback(_ping_db, int(options.mysql_recycle) * 1000).start()

import logging
import traceback

import tormysql
from tormysql import DictCursor
from tornado import gen
from tornado.gen import coroutine


class AsyncMysqlClient(object):
    def __init__(self, db=None):

        if db:
            _db = db
        else:
            _db = options.mysql_database

        self.pool = tormysql.ConnectionPool(
            max_connections=20,
            host = options.mysql_host,
            port = options.mysql_port,
            user = options.mysql_user,
            password = options.mysql_password,
            db = _db,
            autocommit=True,
            charset = 'utf8',
            idle_seconds= 1800
        )
        super(AsyncMysqlClient, self).__init__()

    @coroutine
    def query_one(self, sql, args=None):
        data = None
        with (yield self.pool.Connection()) as conn:
            try:
                with conn.cursor(cursor_cls=DictCursor) as cursor:
                    yield cursor.execute(sql, args)
                    data = cursor.fetchone()
            except Exception as e:
                logging.error(traceback.print_exc())
                logging.error("Query error: %s", e.args)

        raise gen.Return(data)

    @coroutine
    def query_all(self, sql, args=None):
        datas = None
        with (yield self.pool.Connection()) as conn:
            try:
                with conn.cursor(cursor_cls=DictCursor) as cursor:
                    yield cursor.execute(sql, args)
                    datas = cursor.fetchall()
            except Exception as e:
                logging.error(traceback.print_exc())
                logging.error("Query error: %s", e.args)

        raise gen.Return(datas)

    @coroutine
    def execute(self, sql, args=None):
        with (yield self.pool.Connection()) as conn:
            try:
                with conn.cursor(cursor_cls=DictCursor) as cursor:
                    ret = yield cursor.execute(sql, args)
            except Exception as e:
                logging.error(traceback.print_exc())
                logging.error("Query error: %s", e.args)
                yield conn.rollback()
            else:
                yield conn.commit()

        raise gen.Return(ret)

    @coroutine
    def execute_many(self, sql, args=None):
        with (yield self.pool.Connection()) as conn:
            try:
                with conn.cursor(cursor_cls=DictCursor) as cursor:
                    ret = yield cursor.executemany(sql, args)
            except Exception as e:
                logging.error(traceback.print_exc())
                logging.error("Query error: %s", e.args)
                yield conn.rollback()
            else:
                yield conn.commit()

        raise gen.Return(ret)


def connect(db=None):
    async_mysql_client = AsyncMysqlClient(db)
    return async_mysql_client
