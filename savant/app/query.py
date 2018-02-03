import sys
import json, flask
import os
import psycopg2
from sqlalchemy import create_engine
from app import app
from app.base_path import get_path
from app import get_scanned

class Query:
    def __init__(self):

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

    def record_flavors(self):

        self.cur.execute("select store_datetime()")
        self.cur.executemany("select store_debs(%s, %s ,%s, %s)", get_scanned.debs)
        self.cur.executemany("select store_groups(%s, %s, %s, %s)", get_scanned.groups)
        self.cur.executemany("select store_shadow(%s, %s, %s, %s, %s, %s, %s, %s, %s)", get_scanned.shadow)
        self.cur.executemany("select store_users(%s, %s, %s, %s,%s, %s, %s)", get_scanned.users)
        self.conn.commit()

    def record_knowledge(self, json_file, name, resource, action):

        self.cur.execute("select store_knowledge(%s, %s, %s)", (name, resource, action))

        with open(json_file, 'r') as json_res:
            self.res =  json.load(json_res)

        debs = self.res[0]
        new_debs = debs["Debs"]["New"]
        groups = self.res[1]
        new_groups = groups["Groups"]["New"]
        shadow = self.res[2]
        new_shadow = shadow["Shadow"]["New"]
        users = self.res[3]
        new_users = users["Users"]["New"]

        self.knowledge_debs(new_debs)
        self.knowledge_groups(new_groups)
        self.knowledge_shadow(new_shadow)
        self.knowledge_users(new_users)
        self.conn.commit()

    def knowledge_debs(self, new_debs):
        if new_debs[0] != "No changes":
            for self.nd in new_debs:
                self.deb = self.cur.execute("select store_knowledge_debs(%s, %s ,%s, %s)",
                                                                                     (self.nd["Stat"], self.nd["Name"],
                                                                                        self.nd["Version"], self.nd["Architecture"]))

    def knowledge_groups(self, new_groups):
        if new_groups[0] != "No changes":
            for self.ng in new_groups:
                self.cur.execute("select store_knowledge_groups(%s, %s ,%s, %s)",
                                                                        (self.ng["Group Name"], self.ng["Password"],
                                                                         self.ng["Gid"], self.ng["Users"]))

    def knowledge_shadow(self, new_shadow):
        if new_shadow[0] != "No changes":
            for self.ns in new_shadow:
                self.cur.execute("select store_knowledge_shadow(%s, %s ,%s, %s, %s, %s ,%s, %s, %s)",
                                                                                            (self.ns["Username"], self.ns["Password"],
                                                                                            self.ns["Last Changed"],
                                                                                            self.ns["Minimum"], self.ns["Maximum"],
                                                                                            self.ns["Warn"], self.ns["Inactive"],
                                                                                            self.ns["Expire"], self.ns["Reserve"]))

    def knowledge_users(self, new_users):
        if new_users[0] != "No changes":
            for self.nu in new_users:
                self.cur.execute("select store_knowledge_users(%s, %s ,%s, %s, %s, %s, %s )",
                                                                                (self.nu["Username"], self.nu["Password"],
                                                                                self.nu["UID"], self.nu["GID"],
                                                                                self.nu["Description"], self.nu["Path"], self.nu["Shell"]))
    def new_debs(self):

        self.debs = self.cur.execute("select get_debs_unique()")
        self.debs = self.cur.fetchall()
        self.new_debs = []

        if len(self.debs) != 0:
            for self.deb in self.debs:
                d = str(self.deb[0])
                db = d.split(',')
                self.new_debs.append({"Stat" : db[0][1:],
                            "Name" : db[1],
                            "Version" : db[2],
                            "Architecture" : db[3][:len(db[3]) - 1]})
        else:
            self.new_debs.append('No changes')

        self.conn.commit()

        return self.new_debs

    def new_groups(self):

        self.groups = self.cur.execute("select get_groups_unique()")
        self.groups = self.cur.fetchall()
        self.new_groups = []

        if len(self.groups) != 0:
            for self.group in self.groups:
                g = str(self.group[0])
                gr = g.split(',')
                self.new_groups.append({"Group Name" : gr[0][1:],
                                "Password" : gr[1],
                                "Gid" : gr[2],
                                "Users" : gr[3][:len(gr[3]) - 1]})
        else:
            self.new_groups.append('No changes')

        self.conn.commit()

        return self.new_groups

    def new_shadow(self):

        self.shadow = self.cur.execute("select get_shadow_unique()")
        self.shadow = self.cur.fetchall()
        self.new_shadow = []

        if len(self.shadow) != 0:
            for self.shad in self.shadow:
                s = str(self.shad[0])
                sh = s.split(',')
                self.new_shadow.append({"Username" : sh[0][1:],
                                "Password" : sh[1],
                                "Last Changed" : sh[2],
                                "Minimum" : sh[3],
                                "Maximum" : sh[4],
                                "Warn" : sh[5],
                                "Inactive" : sh[6],
                                "Expire" : sh[7],
                                "Reserve" : sh[8][:len(sh[8]) - 1]})
        else:
            self.new_shadow.append('No changes')

        self.conn.commit()
        
        return self.new_shadow

    def new_users(self):

        self.users = self.cur.execute("select get_users_unique()")
        self.users = self.cur.fetchall()
        self.new_users = []

        if len(self.users) != 0:
            for self.user in self.users:
                u = str(self.user[0])
                us = u.split(',')
                self.new_users.append({"Username" : us[0][1:],
                                "Password" : us[1],
                                "UID" : us[2],
                                "GID" : us[3],
                                "Description" : us[4],
                                "Path" : us[5],
                                "Shell" : us[6][:len(us[6]) - 1]})

        else:
            self.new_users.append('No changes')

        self.conn.commit()
        
        return self.new_users

    def execute_sql(self, sql_file):

        self.path = get_path()
        if not self.path.__contains__("/mono/savant/db_script"):
            self.db_directory = self.path + "/mono/savant/db_scripts"
        else:
            self.db_directory = self.path

        os.chdir(self.db_directory)
        self.cur.execute(open(str(sql_file), "r").read())
        self.conn.commit()
