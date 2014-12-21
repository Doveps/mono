from . import common

class Path(object):
    def __init__(self, *args, **kwargs):
        # initialize all fields as None
        (self.inode, self.blocks, self.perms, self.link_count, self.owner,
            self.group, self.size, self.month, self.day,
            self.more_time, self.path, self.link_target) = [None] * 12

        # TODO: allow fields to be passed in __init__

class Paths(common.MergeableDict):
    pass
