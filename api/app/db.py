import sqlite3
from flask import g
from app import application
from app.settings import DATABASE_PATH


class db:

    def get_db(self):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE_PATH)
        return db


    def query_db(self, query, args=(), one=False):
        cur = self.get_db().execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv

    @application.teardown_appcontext
    def close_connection(self, exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()
