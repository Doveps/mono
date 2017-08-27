from flask import Flask, jsonify, request
from utils import SPcalls

spcalls = SPcalls()

def store_debs(stat, name, vers, arch):
    return spcalls.spcall('store_debs', (stat, name, vers, arch,), True)

def store_groups(group_name, password, gid, users):
    return spcalls.spcall('store_groups', (group_name, password, gid, users,), True)

def store_shadow(username, password, lastchanged, minmium, maximum, warn, inactive, expire, reserve):
    return spcalls.spcall('store_shadow', (username, password, lastchanged, minmium, maximum, warn, inactive, expire, reserve,), True)

def store_users(username, password, uid, gid, description, user_path, shell):
    return spcalls.spcall('store_users', (username, password, uid, gid, description, user_path, shell,), True)

def store_debs2(stat, name, vers, arch):
    return spcalls.spcall('store_debs2', (stat, name, vers, arch,), True)

def store_groups2(group_name, password, gid, users):
    return spcalls.spcall('store_groups2', (group_name, password, gid, users,), True)

def store_shadow2(username, password, lastchanged, minmium, maximum, warn, inactive, expire, reserve):
    return spcalls.spcall('store_shadow2', (username, password, lastchanged, minmium, maximum, warn, inactive, expire, reserve,), True)

def store_users2(username, password, uid, gid, description, user_path, shell):
    return spcalls.spcall('store_users2', (username, password, uid, gid, description, user_path, shell,), True)
