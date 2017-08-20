import sys
import json, flask
import os
from sqlalchemy import create_engine
from app import app


# connection = 'local' #or change it to local if you're running on local machine

# if connection == 'local':
    
class DBconn():
    def __init__(self):
        engine = create_engine("postgresql://postgres:postgres@127.0.0.1:5432/travis_ci_test")
        self.conn = engine.connect()
        self.trans = self.conn.begin()


    def getcursor(self):
        cursor = self.conn.connection.cursor()
        return cursor


    def dbcommit(self):
        self.trans.commit()


class SPcalls:
    def __init__(self):
        pass

    def spcall(self, qry, param, commit=False):
        qry = qry
        param = param

        try:
            dbo = DBconn()
            cursor = dbo.getcursor()
            cursor.callproc(qry, param)
            res = cursor.fetchall()
            if commit:
                dbo.dbcommit()
            return res

        except:
            res = [("Error: " + str(sys.exc_info()[0]) + " " + str(sys.exc_info()[1]),)]
            print "res", res
        return res

@app.after_request
def add_cors(resp):
    resp.headers['Access-Control-Allow-Origin'] = flask.request.headers.get('Origin', '*')
    resp.headers['Access-Control-Allow-Credentials'] = True
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET, PUT, DELETE'
    resp.headers['Access-Control-Allow-Headers'] = flask.request.headers.get('Access-Control-Request-Headers',
                                                                             'Authorization')
    # set low for debugging
    if app.debug:
        resp.headers["Access-Control-Max-Age"] = '1'
    return resp
