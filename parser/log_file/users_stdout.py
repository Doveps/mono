from . import common
from systems import user

class UsersStdoutLog(common.Log):

    def parse(self):
        self.logger.debug('parsing')

        self.users = user.Users()
        with open(self.path, 'r') as f:
            for line in f.readlines():
                parts = line.rstrip('\n').split(':')
                assert len(parts) is 7

                (user_name, password, uid, gid, description, path, shell) = parts[0:7]

                assert user_name not in self.users

                self.users[user_name] = user.User()
                self.users[user_name].add_passwd(password, uid, gid,
                        description, path, shell)

    def record(self, flavor):
        self.logger.debug('recording %d users',len(self.users))
        flavor.record('users', self.users)
