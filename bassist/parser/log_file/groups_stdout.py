# Copyright (c) 2015 Kurt Yoder
# See the file LICENSE for copying permission.
from . import common
from ...systems import group

class GroupsStdoutLog(common.Log):

    def parse(self):
        self.logger.debug('parsing')

        self.data = group.Groups()
        self.name = 'groups'

        with open(self.path, 'r') as f:
            for line in f.readlines():
                parts = line.rstrip('\n').split(':')
                assert len(parts) is 4

                (group_name, password, gid, users) = parts[0:4]

                assert group_name not in self.data

                self.data[group_name] = group.Group(password, gid)

                # avoid setting users to '' if there are no users
                users = users.split(',')
                if len(users) is 1 and users[0] is '': continue

                self.data[group_name].add_users(users)
