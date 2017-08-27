from flask import Flask, jsonify, request
from utils import SPcalls

spcalls = SPcalls()

def deb_exists(stat, name, vers, arch):
    return spcalls.spcall('deb_exists', (stat, name, vers, arch,), True)

def group_exists(group_name, password, gid, users):
    return spcalls.spcall('group_exists', (group_name, password, gid, users,), True)

def shadow_exists(username, password, lastchanged, minimum, maximum, warn, inactive, expire, reserve):
    return spcalls.spcall('shadow_exists', (username, password, lastchanged, minimum, maximum, warn, inactive, expire, reserve,), True)

def user_exists(username, password, uid, gid, description, user_path, shell):
    return spcalls.spcall('user_exists', (username, password, uid, gid, description, user_path, shell,), True)

def deb2_exists(stat, name, vers, arch):
    return spcalls.spcall('deb2_exists', (stat, name, vers, arch,), True)

def group2_exists(group_name, password, gid, users):
    return spcalls.spcall('group2_exists', (group_name, password, gid, users,), True)

def shadow2_exists(username, password, lastchanged, minimum, maximum, warn, inactive, expire, reserve):
    return spcalls.spcall('shadow2_exists', (username, password, lastchanged, minimum, maximum, warn, inactive, expire, reserve,), True)

def user2_exists(username, password, uid, gid, description, user_path, shell):
    return spcalls.spcall('user2_exists', (username, password, uid, gid, description, user_path, shell,), True)
