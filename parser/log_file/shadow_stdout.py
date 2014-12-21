from . import common
from systems import user

class ShadowStdoutLog(common.Log):

    def parse(self):
        self.logger.debug('parsing')

        self.users = user.Users()
        with open(self.path, 'r') as f:
            for line in f.readlines():
                parts = line.rstrip('\n').split(':')
                assert len(parts) is 9

                (user_name, password, lastchanged, minimum, maximum,
                        warn, inactive, expire, reserved) = parts[0:9]

                assert user_name not in self.users

                self.users[user_name] = user.User()
                self.users[user_name].add_shadow(password, lastchanged,
                        minimum, maximum, warn, inactive, expire,
                        reserved)

    def record(self, flavor):
        self.logger.debug('recording %d users',len(self.users))
        flavor.record('users', self.users)
