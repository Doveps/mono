from . import common
from systems import user

class ShadowStdoutLog(common.Log):

    def parse(self):
        self.logger.debug('parsing')

        self.data = user.Users()
        self.name = 'users'

        with open(self.path, 'r') as f:
            for line in f.readlines():
                parts = line.rstrip('\n').split(':')
                assert len(parts) is 9

                (user_name, password, lastchanged, minimum, maximum,
                        warn, inactive, expire, reserved) = parts[0:9]

                assert user_name not in self.data

                self.data[user_name] = user.User()
                self.data[user_name].add_shadow(password, lastchanged,
                        minimum, maximum, warn, inactive, expire,
                        reserved)
