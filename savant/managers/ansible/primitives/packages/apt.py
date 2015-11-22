# Copyright (c) 2015 Kurt Yoder
# See the file LICENSE for copying permission.
import logging

class Apt(object):
    def __init__(self, name):
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)
        self.name = name

    def as_directive(self):
        directive = {
                'name': self.name,
                'state': 'present',
                }
        return({'apt': directive})
