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


def get_items(filename):
    if str(filename.filename).__contains__("debs"):
        get_debs(filename)

    elif str(filename.filename).__contains__("groups"):
        get_groups(filename)

    elif str(filename.filename).__contains__("shadow"):
        get_shadow(filename)

    elif str(filename.filename).__contains__("users"):
        get_users(filename)

def get_debs(filename):
    content = []

    for line in filename:
        content.append(line)

    for data in content[5:]:
        parts = data.split()

        (stat, name, vers, arch) = parts[0:4]
        debs.append(parts[0:4])

def get_groups(filename):
    content = []

    for line in filename:
        content.append(line)

        for data in content:
            parts = data.rstrip('\n').split(':')

            (group_name, password, gid, users) = parts[0:4]

            groups.append(parts[0:4])

def get_shadow(filename):
    content = [] 

    for line in filename:
        content.append(line)

    for data in content:
        parts = data.rstrip('\n').split(':')

        (user_name, password, lastchanged, minimum, maximum,
                        warn, inactive, expire, reserved) = parts[0:9]

        shadow.append(parts[0:9])

def get_users(filename):
    content = []


    for line in filename:
        content.append(line)

    for data in content:
        parts = data.rstrip('\n').split(':')

        (user_name, password, uid, gid, description, path, shell) = parts[0:7]

        users.append(parts[0:7])