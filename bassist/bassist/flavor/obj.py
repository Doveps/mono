# Copyright (c) 2015 Kurt Yoder
# See the file LICENSE for copying permission.
import logging

import persistent
import transaction

from ..diff import system

module_logger = logging.getLogger(__name__)

class FlavorObjException(Exception):
    pass

class Obj(persistent.Persistent):
    '''Flavor objects store a collection of systems, for example
    packages, users, and files. If they are instantiated with a UUID,
    they may persist within zodb. Otherwise, they are anonymous and may
    not persist within zodb.'''
    def __init__(self, uuid=None):
        self.uuid = uuid
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)

        if self.uuid is None:
            self.anonymous = True
            self.logger.debug('creating new anonymous flavor')
        else:
            self.anonymous = False
            self.logger.debug('creating new flavor with uuid: %s',self.uuid)

        self.systems = {}
        self.metadata = {}

    def __getstate__(self):
        """logger can not be pickled, so exclude it."""
        assert self.uuid is not None
        out_dict = self.__dict__.copy()
        del out_dict['logger']
        return(out_dict)

    def __setstate__(self, dict):
        """Restore logger which was excluded from pickling."""
        self.__dict__.update(dict)
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)

    def record_metadata(self, metadata_key, data):
        self.logger.debug('setting metadata %s',metadata_key)
        self.metadata[metadata_key] = data

        if not self.anonymous:
            self._p_changed = 1
            transaction.commit()

    def record_system(self, system_name, data):
        if system_name in self.systems:
            self.logger.debug('merging system %s',system_name)
            self.systems[system_name].merge(data)
        else:
            self.logger.debug('setting system %s',system_name)
            self.systems[system_name] = data

        if not self.anonymous:
            self._p_changed = 1
            transaction.commit()

    def diff_system(self, system_name, new_data):
        if system_name not in self.systems:
            return system.System(new_data)

        return system.System(self.systems[system_name], new_data)

def get(db, uuid):
    if not uuid in db:
        module_logger.debug('creating new object from uuid: %s',uuid)
        db[uuid] = Obj(uuid)
        transaction.commit()
    return(db[uuid])
