class Stripped(object):
    def __init__(self, diff):
        self.data = {}

        for sys_name, system in diff.system_diffs.items():
            self.data[sys_name] = {'subtract': {}, 'add': {}}
            for diff_name, diff_obj in system.only_in_data1.items():
                self.data[sys_name]['subtract'][diff_name] = diff_obj
            for diff_name, diff_obj in system.only_in_data2.items():
                self.data[sys_name]['add'][diff_name] = diff_obj

    def __repr__(self):
        return '<%s %s>'%(type(self).__name__, self.data)

