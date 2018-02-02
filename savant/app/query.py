import sys
import json, flask
import os
import psycopg2
from sqlalchemy import create_engine
from app import app
from app.base_path import get_path
from app import get_scanned

# def set_engine_name():
#     global conn, cur

#     path = get_path() + "/mono/savant/app"
#     os.chdir(path)

#     with open('db_config.json', 'r') as db_file:
#         db_info = json.load(db_file)

#     db_name = db_info["database"]["database_name"]
#     username = db_info["database"]["username"]
#     password = db_info["database"]["password"]
#     host = db_info["database"]["host"]
#     engine_name = "postgresql://" + username + ":" + password + "@" + host + ":5432/" + db_name

#     conn = psycopg2.connect(engine_name)
#     cur = conn.cursor()

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

class Query:
    def __init__(self):
        # global conn, cur

        self.path = get_path() + "/mono/savant/app"
        os.chdir(self.path)

        with open('db_config.json', 'r') as db_file:
            db_info = json.load(db_file)

        self.db_name = db_info["database"]["database_name"]
        self.username = db_info["database"]["username"]
        self.password = db_info["database"]["password"]
        self.host = db_info["database"]["host"]
        self.engine_name = "postgresql://" + self.username + ":" + self.password + "@" + self.host + ":5432/" + self.db_name

        self.conn = psycopg2.connect(self.engine_name)
        self.cur = self.conn.cursor()

    # def set_engine_name(self):
    #     global conn, cur

    #     path = get_path() + "/mono/savant/app"
    #     os.chdir(path)

    #     with open('db_config.json', 'r') as db_file:
    #         db_info = json.load(db_file)

    #     db_name = db_info["database"]["database_name"]
    #     username = db_info["database"]["username"]
    #     password = db_info["database"]["password"]
    #     host = db_info["database"]["host"]
    #     engine_name = "postgresql://" + username + ":" + password + "@" + host + ":5432/" + db_name

    #     conn = psycopg2.connect(engine_name)
    #     cur = conn.cursor()

    def record_flavors(self):
        # set_engine_name()

        self.cur.execute("select store_datetime()")
        self.cur.executemany("select store_debs(%s, %s ,%s, %s)", get_scanned.debs)
        self.cur.executemany("select store_groups(%s, %s, %s, %s)", get_scanned.groups)
        self.cur.executemany("select store_shadow(%s, %s, %s, %s, %s, %s, %s, %s, %s)", get_scanned.shadow)
        self.cur.executemany("select store_users(%s, %s, %s, %s,%s, %s, %s)", get_scanned.users)    

        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def record_knowledge(self, json_file, name, resource, action):
        # set_engine_name()

        self.cur.execute("select store_knowledge(%s, %s, %s)", (name, resource, action))

        with open(json_file, 'r') as json_res:
            self.res =  json.load(json_res)

        debs = res[0]
        new_debs = debs["Debs"]["New"]
        groups = res[1]
        new_groups = groups["Groups"]["New"]
        shadow = res[2]
        new_shadow = shadow["Shadow"]["New"]
        users = res[3]
        new_users = users["Users"]["New"]

        knowledge_debs(new_debs)
        knowledge_groups(new_groups)
        knowledge_shadow(new_shadow)
        knowledge_users(new_users)

        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def knowledge_debs(new_debs):
        if new_debs[0] != "No changes":
            for nd in new_debs:
                deb = cur.execute("select store_knowledge_debs(%s, %s ,%s, %s)", (nd["Stat"], nd["Name"], nd["Version"], nd["Architecture"]))

    def knowledge_groups(new_groups):
        if new_groups[0] != "No changes":
            for ng in new_groups:
                cur.execute("select store_knowledge_groups(%s, %s ,%s, %s)", (ng["Group Name"], ng["Password"], ng["Gid"], ng["Users"]))

    def knowledge_shadow(new_shadow):
        if new_shadow[0] != "No changes":

            for ns in new_shadow:
                cur.execute("select store_knowledge_shadow(%s, %s ,%s, %s, %s, %s ,%s, %s, %s)", (ns["Username"], ns["Password"],
                                                                                            ns["Last Changed"], ns["Minimum"],
                                                                                            ns["Maximum"],
                                                                                            ns["Warn"], ns["Inactive"],
                                                                                            ns["Expire"], ns["Reserve"]))

    def knowledge_users(new_users):
        if new_users[0] != "No changes":
            for nu in new_users:
                cur.execute("select store_knowledge_users(%s, %s ,%s, %s, %s, %s, %s )", (nu["Username"], nu["Password"],
                                                                                    nu["UID"], nu["GID"],
                                                                                    nu["Description"], nu["Path"], nu["Shell"]))
    def new_debs(self):
        # set_engine_name()

        self.debs = self.cur.execute("select get_debs_unique()")
        self.debs = self.cur.fetchall()
        self.new_debs = []

        if len(self.debs) != 0:
            for self.deb in debs:
                d = str(deb[0])
                db = d.split(',')
                self.new_debs.append({"Stat" : db[0][1:],
                            "Name" : db[1],
                            "Version" : db[2],
                            "Architecture" : db[3][:len(db[3]) - 1]})
        else:
            self.new_debs.append('No changes')

        self.conn.commit()
        self.cur.close()
        self.conn.close()

        return self.new_debs

    def new_groups():
        # set_engine_name()

        groups = cur.execute("select get_groups_unique()")
        groups = cur.fetchall()
        new_groups = []

        if len(groups) != 0:
            for group in groups:
                g = str(group[0])
                gr = g.split(',')
                new_groups.append({"Group Name" : gr[0][1:],
                                "Password" : gr[1],
                                "Gid" : gr[2],
                                "Users" : gr[3][:len(gr[3]) - 1]})
        else:
            new_groups.append('No changes')

        conn.commit()
        cur.close()
        conn.close()

        return new_groups

    def new_shadow():
        # set_engine_name()

        shadow = cur.execute("select get_shadow_unique()")
        shadow = cur.fetchall()
        new_shadow = []

        if len(shadow) != 0:
            for shad in shadow:
                s = str(shad[0])
                sh = s.split(',')
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
            new_shadow.append('No changes')

        conn.commit()
        cur.close()
        conn.close()
        
        return new_shadow

    def new_users():
        # set_engine_name()

        users = cur.execute("select get_users_unique()")
        users = cur.fetchall()
        new_users = []

        if len(users) != 0:
            for user in users:
                u = str(user[0])
                us = u.split(',')
                new_users.append({"Username" : us[0][1:],
                                "Password" : us[1],
                                "UID" : us[2],
                                "GID" : us[3],
                                "Description" : us[4],
                                "Path" : us[5],
                                "Shell" : us[6][:len(us[6]) - 1]})

        else:
            new_users.append('No changes')

        conn.commit()
        cur.close()
        conn.close()

        return new_users
