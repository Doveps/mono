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
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)

        engine = create_engine("postgresql://postgres:postgres@localhost:5432/doveps", echo=False)
        self.connection = psycopg2.connect("dbname=doveps user=postgres password=postgres")
        self.cursor = self.connection.cursor()

    def get_or_create_tables(self):
        # Todo: Make sure that the tables are created
        pass

    def record_flavor(self, name):
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

    def get_id_from_name(self, flavor_name):
        """Check if the flavor name has a flavor ID. If not, create it.
        Then return the flavor ID."""
        self.logger.debug('flavor_name: %s', flavor_name)
        self.cursor.execute("SELECT * FROM flavors where name = %s", flavor_name)
        name_obj = self.cursor.fetchone()[0]
        return (name_obj)

    def get_obj_from_id(self, flavor_id):
        """Check if the flavor object referenced by the given ID exists. If
        not, create it. Then return the flavor object."""
        self.logger.debug('flavor_id: %s', flavor_id)
        self.cursor.execute("SELECT * FROM flavors where id = %s", flavor_id)
        obj = self.cursor.fetchone()[0]
        return (obj)
