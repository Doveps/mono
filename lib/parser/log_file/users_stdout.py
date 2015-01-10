from . import common
from ...systems import user

class UsersStdoutLog(common.Log):

    def parse(self):
        self.logger.debug('parsing')

        self.data = user.Users()
        self.name = 'users'

        with open(self.path, 'r') as f:
            for line in f.readlines():
                parts = line.rstrip('\n').split(':')
                assert len(parts) is 7

                (user_name, password, uid, gid, description, path, shell) = parts[0:7]

                # TODO: passwd spec does allow duplicate names, but not IDs!
                assert user_name not in self.data

                self.data[user_name] = user.User()
                self.data[user_name].add_passwd(password, uid,
                        gid, description, path, shell)
