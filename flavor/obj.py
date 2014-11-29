import logging

import persistent
import transaction

module_logger = logging.getLogger(__name__)

class FlavorObjException(Exception):
    pass

class Obj(persistent.Persistent):
    def __init__(self, uuid):
        self.uuid = uuid
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)
        self.logger.debug('creating object from uuid %s',self.uuid)

    def __getstate__(self):
        """logger can not be pickled, so exclude it."""
        out_dict = self.__dict__.copy()
        del out_dict['logger']
        return(out_dict)

    def __setstate__(self, dict):
        """Restore logger which was excluded from pickling."""
        self.__dict__.update(dict)
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)

def get(db, uuid):
    if not uuid in db:
        module_logger.debug('creating new object from uuid: %s',uuid)
        db[uuid] = Obj(uuid)
        transaction.commit()
    return(db[uuid])
