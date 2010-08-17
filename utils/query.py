# -*- coding: utf-8 -*-



class SQLQuery(object):
    result_action = 'fetchall'
    result = None
    auto_commit = True

    def __init__(self, name, sql, params=()):
        if self.result_action not in ('fetchall', 'fetchone', 'execute'):
            raise TypeError('Bad `result_action` value')
        self.name = name
        self.sql = sql
        self.params = params

    def _fetch_data(self, cursor):
        cursor.execute(self.sql, self.params)
        if self.result_action == 'fetchall':
            self.result = cursor.fetchall()
        elif self.result_action == 'fetchone':
            self.resul = cursor.fetchone()
