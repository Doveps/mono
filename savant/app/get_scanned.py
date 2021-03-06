import os
from bassist.parser import host as parser_host
import logging
import logging.config
# from app import record

debs = [] 
groups = []
shadow = []
users = []

def parse(scanner_directory):
    logger = logging.getLogger(__name__)
    logger.debug('importing parsers')
    parsed_host = parser_host.Host(scanner_directory)
    logger.debug('finished importing parsers')

    for parser in parsed_host.parsers:
        logger.debug('parser log: %s', parser.log)
        logger.debug('parsing: %s', parser.path)
        parser.parse()

def get_items(filenames):
    for filename in filenames:
        if "debs" in str(filename.filename):
            get_debs(filename)

        elif "groups" in str(filename.filename):
            get_groups(filename)

        elif "shadow" in str(filename.filename):
            get_shadow(filename)

        elif "users" in str(filename.filename):
            get_users(filename)

def replace_blank(parts):
    for i in xrange(len(parts)):
        if parts[i] == '':
            parts[i] = None

    return parts



def get_debs(filename):
    del debs[:]
    content = []

    for line in filename:
        content.append(line)

    for data in content[5:]:
        parts = data.split()

        (stat, name, vers, arch) = parts[0:4]

        parts[0:4] = replace_blank(parts[0:4])
        debs.append(parts[0:4])


def get_groups(filename):
    del groups[:]
    content = []

    for line in filename:
        content.append(line)

    for data in content:
        parts = data.rstrip('\n').split(':')

        (group_name, password, gid, users) = parts[0:4]

        parts[0:4] = replace_blank(parts[0:4])
        groups.append(parts[0:4])


def get_shadow(filename):
    del shadow[:]
    content = [] 

    for line in filename:
        content.append(line)

    for data in content:
        parts = data.rstrip('\n').split(':')

        (user_name, password, lastchanged, minimum, maximum,
                        warn, inactive, expire, reserved) = parts[0:9]

        parts[0:9] = replace_blank(parts[0:9])
        shadow.append(parts[0:9])


def get_users(filename):
    del users[:]
    content = []


    for line in filename:
        content.append(line)

    for data in content:
        parts = data.rstrip('\n').split(':')

        (user_name, password, uid, gid, description, path, shell) = parts[0:7]

        parts[0:7] = replace_blank(parts[0:7])
        users.append(parts[0:7])
