# Copyright (c) 2015 Kurt Yoder
# See the file LICENSE for copying permission.
import logging
import uuid

import persistent
import transaction

module_logger = logging.getLogger(__name__)

class FlavorNameException(Exception):
    pass

class Name(persistent.Persistent):
    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)
        self.logger.debug('creating flavor %s',self.name)
        self.uuid = str(uuid.uuid4())
        self.logger.debug('uuid is %s',self.uuid)

    def __getstate__(self):
        """logger can not be pickled, so exclude it."""
        out_dict = self.__dict__.copy()
        del out_dict['logger']
        return(out_dict)

    def __setstate__(self, dict):
        """Restore logger which was excluded from pickling."""
        self.__dict__.update(dict)
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)

def get(db, name):
    if not name in db:
        module_logger.debug('creating new name: %s',name)
        db[name] = Name(name)
        transaction.commit()
    return(db[name])
