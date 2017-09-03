import os
from flask import jsonify, request
from app import record, get_scanned
from run_sql import execute_sql
from utils import SPcalls
from app.base_path import get_path

spcalls = SPcalls()

def new_debs():
    debs = spcalls.spcall('get_debs2_unique', ())
    new_debs = []

    if len(debs) != 0:
        for deb in debs:
            new_debs.append({"Stat" : deb[0],
                            "Name" : deb[1],
                            "Version" : deb[2],
                            "Architecture" : deb[3]})
    else:
        new_debs.append('No changes')

    return new_debs

def new_groups():
    groups = spcalls.spcall('get_groups2_unique', ())
    new_groups = []

    if len(groups) != 0:
        for group in groups:
            new_groups.append({"Group Name" : group[0],
                                "Password" : group[1],
                                "Gid" : group[2],
                                "Users" : group[3]})
    else:
        new_groups.append('No changes')

    return new_groups

def new_shadow():
    shadow = spcalls.spcall('get_shadow2_unique', ())
    new_shadow = []

    if len(shadow) != 0:
        for shad in shadow:
            new_shadow.append({"Username" : shad[0],
                            "Password" : shad[1],
                            "Last Changed" : shad[2],
                            "Minimum" : shad[3],
                            "Maximum" : shad[4],
                            "Warn" : shad[5],
                            "Inactive" : shad[6],
                            "Expire" : shad[7],
                            "Reserve" : shad[8]})

    else:
        new_shadow.append('No changes')

    return new_shadow

def new_users():
    users = spcalls.spcall('get_users2_unique', ())
    new_users = []

    if len(users) != 0:
        for user in users:
            new_users.append({"Username" : shad[0],
                            "Password" : shad[1],
                            "UID" : shad[2],
                            "GID" : shad[3],
                            "Description" : shad[4],
                            "Path" : shad[5],
                            "Shell" : shad[6]})

    else:
        new_users.append('No changes')

    return new_users
