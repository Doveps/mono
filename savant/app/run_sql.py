import psycopg2, json
import sys
import os 
from app.base_path import get_path

def execute_sql(sql_file):
    path = get_path() + "/mono/savant/app"
    os.chdir(path)

    with open('db_config.json', 'r') as db_file:
        db_info = json.load(db_file)

    db_name = db_info["database"]["database_name"]
    username = db_info["database"]["username"]
    password = db_info["database"]["password"]
    host = db_info["database"]["host"]
    engine_name = "postgresql://" + username + ":" + password + "@" + host + ":5432/" + db_name
    conn = psycopg2.connect(engine_name)
    cur = conn.cursor()

    path = get_path()
    if not path.__contains__("/mono/savant/db_script"):
        db_directory = path + "/mono/savant/db_scripts"
    else:
        db_directory = path

    os.chdir(db_directory)
    cur.execute(open(str(sql_file), "r").read())
    conn.commit()
