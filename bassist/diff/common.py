class Diff(object):

    def different(self):
        for val in self.matches.values():
            if val is False:
                return True

        return False

    def set_mismatch(self, kind):
        self.matches[kind] = False

    def set_match(self, kind):
        self.matches[kind] = True
