import sys
import json, flask
import os
import psycopg2
from sqlalchemy import create_engine
from app import app
from app.base_path import get_path
from app import get_scanned

def set_engine_name():
    global conn, cur

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

def execute_sql(sql_file):
    set_engine_name()

    path = get_path()
    if not path.__contains__("/mono/savant/db_script"):
        db_directory = path + "/mono/savant/db_scripts"
    else:
        db_directory = path

    os.chdir(db_directory)
    cur.execute(open(str(sql_file), "r").read())
    conn.commit()
    cur.close()
    conn.close()

def record_base_flavors():
    set_engine_name()

    cur.execute("select store_datetime()")
    cur.executemany("select store_debs(%s, %s ,%s, %s)", get_scanned.debs)
    cur.executemany("select store_groups(%s, %s, %s, %s)", get_scanned.groups)
    cur.executemany("select store_shadow(%s, %s, %s, %s, %s, %s, %s, %s, %s)", get_scanned.shadow)
    cur.executemany("select store_users(%s, %s, %s, %s,%s, %s, %s)", get_scanned.users)    

    conn.commit()
    cur.close()
    conn.close()

def record_comparison_flavors():
    set_engine_name()

    cur.executemany("select store_debs2(%s, %s ,%s, %s)", get_scanned.debs)
    cur.executemany("select store_groups2(%s, %s, %s, %s)", get_scanned.groups)
    cur.executemany("select store_shadow2(%s, %s, %s, %s, %s, %s, %s, %s, %s)", get_scanned.shadow)
    cur.executemany("select store_users2(%s, %s, %s, %s,%s, %s, %s)", get_scanned.users)    

    conn.commit()
    cur.close()
    conn.close()

def record_knowledge():
    set_engine_name()
    
    if resource == 'Debs':
        cur.execute("select get_debs_id('" + name + "')")
    elif resource == 'Groups':
        cur.execute("select get_groups_id('" + name + "')")
    elif resource == 'Shadow':
        cur.execute("select get_shadow_id('" + name + "')")
    elif resource == 'Users':
        cur.execute("select get_users_id('" + name + "')")
        
    name_id = cur.fetchone()[0]
    name_id = int(name_id)

    cur.execute("select store_knowledge(%s, %s, %s, %s)", (name, resource, action, name_id))

    conn.commit()
    cur.close()
    conn.close()

def new_debs():
    set_engine_name()

    debs = cur.execute("select get_debs2_unique()")
    debs = cur.fetchall()
    new_debs = []

    if len(debs) != 0:
        for deb in debs:
            d = str(deb[0])
            db = d.split(',')
            if db[3] is None:
                new_debs.append({"Stat" : db[0][1:],
                                "Name" : db[1],
                                "Version" : db[2],
                                "Architecture" : db[3][:len(db[3]) - 1]})
            else:
                new_debs.append({"Stat" : db[0][1:],
                                "Name" : db[1],
                                "Version" : db[2],
                                "Architecture" : db[3]})
    else:
        new_debs.append('No changes')

    conn.commit()
    cur.close()
    conn.close()

    return new_debs

def new_groups():
    set_engine_name()

    groups = cur.execute("select get_groups2_unique()")
    groups = cur.fetchall()
    new_groups = []

    if len(groups) != 0:
        for group in groups:
            g = str(group[0])
            gr = g.split(',')
            if gr[3] is None:
                new_groups.append({"Group Name" : gr[0][1:],
                                    "Password" : gr[1],
                                    "Gid" : gr[2],
                                    "Users" : gr[3][:len(gr[3]) - 1]})
            else:
                new_groups.append({"Group Name" : gr[0][1:],
                                    "Password" : gr[1],
                                    "Gid" : gr[2],
                                    "Users" : gr[3]})
    else:
        new_groups.append('No changes')

    conn.commit()
    cur.close()
    conn.close()

    return new_groups

def new_shadow():
    set_engine_name()

    shadow = cur.execute("select get_shadow2_unique()")
    shadow = cur.fetchall()
    new_shadow = []

    if len(shadow) != 0:
        for shad in shadow:
            s = str(shad[0])
            sh = s.split(',')
            if sh[8] is None:
                new_shadow.append({"Username" : sh[0][1:],
                                "Password" : sh[1],
                                "Last Changed" : sh[2],
                                "Minimum" : sh[3],
                                "Maximum" : sh[4],
                                "Warn" : sh[5],
                                "Inactive" : sh[6],
                                "Expire" : sh[7],
                                "Reserve" : sh[8][:len(sh[8]) - 1]})
            else:
                new_shadow.append({"Username" : sh[0][1:],
                                "Password" : sh[1],
                                "Last Changed" : sh[2],
                                "Minimum" : sh[3],
                                "Maximum" : sh[4],
                                "Warn" : sh[5],
                                "Inactive" : sh[6],
                                "Expire" : sh[7],
                                "Reserve" : sh[8]})
    else:
        new_shadow.append('No changes')

    conn.commit()
    cur.close()
    conn.close()
        
    return new_shadow

def new_users():
    set_engine_name()

    users = cur.execute("select get_users2_unique()")
    users = cur.fetchall()
    new_users = []

    if len(users) != 0:
        for user in users:
            u = str(user[0])
            us = u.split(',')
            if us[6] is None:
                new_users.append({"Username" : us[0][1:],
                                "Password" : us[1],
                                "UID" : us[2],
                                "GID" : us[3],
                                "Description" : us[4],
                                "Path" : us[5],
                                "Shell" : us[6][len(us[6]) - 1]})
            else:
                new_users.append({"Username" : us[0][1:],
                                "Password" : us[1],
                                "UID" : us[2],
                                "GID" : us[3],
                                "Description" : us[4],
                                "Path" : us[5],
                                "Shell" : us[6]})

    else:
        new_users.append('No changes')

    conn.commit()
    cur.close()
    conn.close()

    return new_users
