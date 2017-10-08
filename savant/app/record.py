import os
import json
from app import app
from app.base_path import get_path
from app import get_scanned
import store_data, check_exists
import psycopg2
import timeit



def record_base_flavors():
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

    cur.executemany("select store_debs(%s, %s ,%s, %s)", get_scanned.debs)
    group_start_time = timeit.default_timer()
    cur.executemany("select store_groups(%s, %s, %s, %s)", get_scanned.groups)
    cur.executemany("select store_shadow(%s, %s, %s, %s, %s, %s, %s, %s, %s)", get_scanned.shadow)
    cur.executemany("select store_users(%s, %s, %s, %s,%s, %s, %s)", get_scanned.users)
    
    conn.commit()
    cur.close()
    conn.close()

def record_comparison_flavors():
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

    cur.executemany("select store_debs2(%s, %s ,%s, %s)", get_scanned.debs)
    group_start_time = timeit.default_timer()
    cur.executemany("select store_groups2(%s, %s, %s, %s)", get_scanned.groups)
    cur.executemany("select store_shadow2(%s, %s, %s, %s, %s, %s, %s, %s, %s)", get_scanned.shadow)
    cur.executemany("select store_users2(%s, %s, %s, %s,%s, %s, %s)", get_scanned.users)
    
    conn.commit()
    cur.close()
    conn.close()