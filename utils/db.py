# -*- coding: utf-8 -*-


import configuration

import psycopg2
from psycopg2 import extensions
from psycopg2.extras import DictCursor

import gevent
from gevent import socket



def wait_callback(conn, timeout=None):
    while 1:
        state = conn.poll()
        if state == extensions.POLL_OK:
            return
        elif state == extensions.POLL_READ:
            socket.wait_read(conn.fileno(), timeout=timeout)
        elif state == extensions.POLL_WRITE:
            socket.wait_write(conn.fileno(), timeout=timeout)
        else:
            raise psycopg2.OperationalError(
                "Bad result from poll: %r" % state)

extensions.set_wait_callback(wait_callback)


class DbPool(object):
    connection_max_age = 60 * 5

    def __init__(self, max_cached_connections=100):
        self.connections = []
        self.max_cached_connections = max_cached_connections

    def get(self):
        if self.connections:
            conn = self.connections.pop()
        else:
            conn = psycopg2.connect(**configuration.DATABASES['default'])
        return conn

    def free(self, conn):
        try:
            # just in case of junks
            conn.rollback()
        except:
            pass
        if len(self.connections) > self.max_cached_connections:
            conn.close()
        else:
            self.connections.append(conn)

db_pool = DbPool()

def _fetch(sql_query):
    q = sql_query
    conn = db_pool.get()
    cursor = conn.cursor(cursor_factory=DictCursor)
    try:
        cursor.execute(q.sql, q.params)
        r = getattr(cursor, q.result_action)()
        q.result = r
    except:
        conn.rollback()
        raise
    finally:
        if q.auto_commit:
            conn.commit()
        cursor.close()
        db_pool.free(conn)
    return q

def fetch(*queries):
    """Multi DB fetch"""
    workers = []
    for sql_query in queries:
        workers.append(gevent.spawn(_fetch, sql_query))
    gevent.joinall(workers)
    results = {}
    for worker in workers:
        if worker.value.name in results:
            raise NameError("SQLQeury name duplicate: %s" % worker.value.name)
        results[worker.value.name] = worker.value.result
    return results
