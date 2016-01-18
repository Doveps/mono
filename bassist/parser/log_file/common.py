# Copyright (c) 2015, 2016 Kurt Yoder
# See the file LICENSE for copying permission.
import logging
import time
import re

from ... import interview

class Observer(object):
    '''Artifacts that result from running the observer (e.g. Ansible) will be
    recorded here. Some of the parsers need to ignore them since they are not
    useful for determining diffs between systems.'''

    # .ansible/tmp/ansible-tmp-1417897614.23-199064374829668
    # It is as of yet unknown how many digits can follow the dot. We have seen
    # 1, 2, and 3. We'll be conservative and expect between one and five
    # digits.
    timestamp_re = re.compile('\.ansible/tmp/ansible-tmp-\d{10,}.\d{1,5}-\d+(/|$)')
    # /bin/sh -c ps -eo pid,ppid,uid,gid,cgroup,f,ni,pri,tty,args -www
    pslist_re = re.compile('^(/bin/sh -c )?ps -eo ([a-z]{1,6},){9,}[a-z]{1,6} -www$')

class ParserLogException(Exception):
    pass

class Log(object):
    def __init__(self, path):
        self.path = path
        self.log = self.__module__.split('.')[-1]
        self.logger = logging.getLogger(self.__module__ + '.' + type(self).__name__)
        self.interview = interview.get()

    def parse(self):
        '''The default parse method does nothing. It should be
        overridden by a subclass method.'''
        self.logger.debug('skipping parse due to empty method')
        pass

    def __repr__(self):
        return '%s: %d'%(self.__class__.__name__, len(self.data))
