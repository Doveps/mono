from . import common

class Passwd(common.NaiveRepr):
    def __init__(self, password, uid, gid, description, path, shell):
        self.password = password
        self.uid = uid
        self.gid = gid
        self.description = description
        self.path = path
        self.shell = shell

class Shadow(common.NaiveRepr):
    def __init__(self, password, lastchanged, minimum, maximum, warn,
            inactive, expire, reserved):
        self.password = password
        self.lastchanged = lastchanged
        self.minimum = minimum
        self.maximum = maximum
        self.warn = warn
        self.inactive = inactive
        self.expire = expire
        self.reserved = reserved

class User(common.NaiveRepr):
    def __init__(self):
        self.passwd = None
        self.shadow = None

    def add_passwd(self, password, uid, gid, description, path, shell):
        self.passwd = Passwd(password, uid, gid, description, path,
                shell)

    def add_shadow(self, password, lastchanged, minimum, maximum, warn,
            inactive, expire, reserved):
        self.shadow = Shadow(password, lastchanged, minimum, maximum,
                warn, inactive, expire, reserved)

    def merge(self, other):
        if other.passwd and not self.passwd:
            self.passwd = other.passwd
        if other.shadow and not self.shadow:
            self.shadow = other.shadow

class Users(common.MergeableDict):
    pass
