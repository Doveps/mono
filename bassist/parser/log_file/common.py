import logging
import time
import re

class Observer(object):
    '''Artifacts that result from running the observer (e.g. Ansible) will be
    recorded here. Some of the parsers need to ignore them since they are not
    useful for determining diffs between systems.'''

    # .ansible/tmp/ansible-tmp-1417897614.23-199064374829668
    timestamp_re = re.compile('\.ansible/tmp/ansible-tmp-\d{10,}.\d{2}-\d+(/|$)')
    # /bin/sh -c ps -eo pid,ppid,uid,gid,cgroup,f,ni,pri,tty,args -www
    pslist_re = re.compile('^(/bin/sh -c )?ps -eo ([a-z]{1,6},){9,}[a-z]{1,6} -www$')

class ParserLogException(Exception):
    pass

class Log(object):
    def __init__(self, path):
        self.path = path
        self.log = self.__module__.split('.')[-1]
        self.logger = logging.getLogger(self.__module__ + '.' + type(self).__name__)

        self.data = None
        self.name = None

    def parse(self):
        '''The default parse method does nothing. It should be
        overridden by a subclass method.'''
        self.logger.debug('skipping parse due to empty method')
        pass

    def record(self, flavor):
        '''The default record method assumes that both attributes "data"
        and "name" have been populated. "data" should contain a zodb
        persistent object, and "name" should contain the name of the
        database key in the zodb. It then invokes "record" on the
        flavor.'''

        assert self.name is not None
        assert self.data is not None

        self.logger.debug('recording %d %s',len(self.data),self.name)

        start_time = time.time()

        flavor.record_system(self.name, self.data)

        self.logger.debug('completed recording in %d seconds',
                time.time() - start_time)

    def diff(self, flavor):

        assert self.name is not None
        assert self.data is not None

        return flavor.diff_system(self.name, self.data)

    def __repr__(self):
        return '%s: %d'%(self.__class__.__name__, len(self.data))
