# Copyright (c) 2015 Kurt Yoder
# See the file LICENSE for copying permission.
import os
import json
import logging

import psycopg2
from sqlalchemy import create_engine

from . import name
from . import obj


class FlavorDBException(Exception):
    pass


class DB(object):
    def __init__(self, path=None):
        print "Hello db_pg"
        # print object
        # table_name = "Flavors"
        # self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)
        # self.connection = psycopg2.connect("dbname='doveps' user='postgres' host='localhost' password='postgres'")
        # print self.connection
        # self.cursor = self.connection.cursor()
        self.cursor.execute("create table if not exists Doveps.flavors(id integer)")
        # self.cursor.execute("""select exists(select * from information_schema.tables where table_name=%s)""" % ("Flavors",))
        # print self.cursor.fetchone()[0]

    def get_or_create_tables(self):
        print "create table"
        # Todo: Make sure that the tables are created

    def record_flavor(self, name):
        print "record flavor"
        """
        :param name:
        :param data:
        :return: id Flavor id
        """
        self.cursor.execute("INSERT INTO Flavor (name) VALUES (%s)", (name,))
        obj = self.cursor.fetchone()[0]
        return obj

    def record_metadata(self, flavor_id, name, data):
        self.cursor.execute("INSERT INTO Metadata (name, data, flavor_id) VALUES (%s, %s, %s)",
                            (name, json.dump(data), flavor_id))
        obj = self.cursor.fetchone()[0]
        return obj

    def close(self):
        self.cursor.close()
        self.connection.close()