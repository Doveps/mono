import logging

import persistent
import transaction

from ..diff import system

module_logger = logging.getLogger(__name__)

class FlavorObjException(Exception):
    pass

class Obj(persistent.Persistent):
    def __init__(self, uuid):
        self.uuid = uuid
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)
        self.logger.debug('new uuid: %s',self.uuid)
        self.systems = {}

    def __getstate__(self):
        """logger can not be pickled, so exclude it."""
        out_dict = self.__dict__.copy()
        del out_dict['logger']
        return(out_dict)

    def __setstate__(self, dict):
        """Restore logger which was excluded from pickling."""
        self.__dict__.update(dict)
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)

    def record_system(self, system_name, data):
        if system_name in self.systems:
            self.logger.debug('merging system %s',system_name)
            self.systems[system_name].merge(data)
        else:
            self.logger.debug('setting system %s',system_name)
            self.systems[system_name] = data
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
