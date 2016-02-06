# Copyright (c) 2016 Kurt Yoder
# See the file LICENSE for copying permission.
import time

import savant.snapshot

_interview = None

class Interview(object):
    '''Link all parsed objects together using an interview.'''

    def __init__(self):
        self.id = time.time()
        self.snapshot = savant.snapshot.Snapshot(self.id)

    def reply(self, obj):
        '''Add an object to the interview.'''
        self.snapshot.add(obj)

def start():
    '''Start a new interview with unique id, and make it globally
    available.'''
    global _interview
    if not _interview:
        _interview = Interview()
    return _interview

def get():
    '''Get an existing interview.'''
    assert _interview is not None
    return _interview
