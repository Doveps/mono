# Copyright (c) 2016 Kurt Yoder
# See the file LICENSE for copying permission.
import logging
logger = logging.getLogger(__name__)

import savant.snapshot

_interview = None

class Interview(object):
    '''Link all parsed objects together using an interview.'''

    def __init__(self, id=None):
        logger.debug('starting interview with id %s',id)
        self.snapshot = savant.snapshot.Snapshot(id)

    def reply(self, obj):
        '''Add an object to the interview.'''
        self.snapshot.add(obj)

    def should_run(self):
        '''Do we already have an interview? If so, don't run again.'''
        if self.snapshot.exists():
            return False
        return True

def start(id=None):
    '''Start a new interview with unique id, and make it globally available.'''
    global _interview
    if not _interview:
        _interview = Interview(id)
    return _interview

def get():
    '''Get an existing interview.'''
    assert _interview is not None
    return _interview
