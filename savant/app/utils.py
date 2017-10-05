import sys
import json, flask
import os
import os
from sqlalchemy import create_engine
from app import app
from app.base_path import get_path

    
class DBconn():
    def __init__(self):

        path = get_path() + "/mono/savant/app"

        os.chdir(path)


        with open('db_config.json', 'r') as db_file:
            db_info = json.load(db_file)

        db_name = db_info["database"]["database_name"]
        username = db_info["database"]["username"]
        password = db_info["database"]["password"]
        host = db_info["database"]["host"]
        engine_name = "postgresql://" + username + ":" + password + "@" + host + ":5432/" + db_name

        engine = create_engine(engine_name)
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
