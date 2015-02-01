import collections

class MergeableDict(collections.MutableMapping):
    '''A dictionary that allows for custom merging behavior.'''

    def __init__(self, *args, **kwargs):
        self.data = dict()
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def merge(self, other):
        for key, val in other.items():
            if key not in self:
                self[key] = val
                continue

            try:
                self[key].merge(val)
            except:
                # if there's no merge, ignore!
                pass

class NaiveRepr(object):
    def __repr__(self):
        return '<%s %s>'%(type(self).__name__, self.__dict__)
