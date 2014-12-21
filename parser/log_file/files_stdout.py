import logging
import shlex
import time

from . import common
from systems import path

class ParsedFileException(Exception):
    pass

class ParsedFileLine(object):
    '''Lines returned by `find . -ls` have an inconsistent format. We
    therefore have to do a bit of computation on the results to
    correlate values with fields. Splitting on spaces is a good first
    guess. However remember that paths can have spaces, and the symlink
    display format ("foo -> bar") also messes with us.

    With that in mind, here is an object to interpret a `find . -ls`
    result line.'''

    logger = logging.getLogger(__name__ + '.ParsedFileLine')

    def __init__(self, line):
        # have to use shlex to split, otherwise escape codes in path
        # mess us up
        self.parts = shlex.split(line)
        self.path = path.Path()

        if len(self.parts) < 11:
            self.set_without_size()

        else:
            self.set_fields_before_path()
            self.set_path(self.parts[10:])

    def set_without_size(self):
        '''Set fields from a line without a size. This is common for 'c'
        files, etc. Note the missing size right before "Oct":
           6320    0 crw-rw-rw-   1 root     root              Oct 19 17:23 /sys/kernel/security/apparmor/.null
        '''
        (self.path.inode, self.path.blocks, self.path.perms,
                self.path.link_count, self.path.owner, self.path.group,
                self.path.month, self.path.day, self.path.more_time,
                self.path.path) = self.parts[0:10]

    def set_fields_before_path(self):
        '''Set fields up to a path:
         523431    4 drwxr-xr-x   9 root     root         4096 Apr 19  2014
        '''
        (self.path.inode, self.path.blocks, self.path.perms,
                self.path.link_count, self.path.owner, self.path.group,
                self.path.size, self.path.month, self.path.day,
                self.path.more_time) = self.parts[0:10]

    def set_path(self, path_parts):
        '''Set a path and possibly also a symlink target. There's room
        for interpretation here because paths can have spaces, and
        symlinks contain spaces due to their 'foo -> bar' format.'''

        count = len(path_parts)
        if count == 1:
            # /opt/VBoxGuestAdditions-4.3.8
            self.path.path = path_parts[0]
            return

        if count == 3:
            if path_parts[1] == '->':
                # /bin/dnsdomainname -> hostname
                self.path.path = path_parts[0]
                self.path.link_target = path_parts[2]
                return

        raise ParsedFileException('Unable to understand path: %s',self.parts)

class FilesStdoutLog(common.Log):
    ignored_top = [ 'dev', 'lost+found', 'proc', 'run', 'sys', 'tmp' ]
    # ignore more?
    #  /home/*/.ansible
    #  /var/log/*

    def parse(self):
        self.logger.debug('parsing')

        self.paths = path.Paths()
        with open(self.path, 'r') as f:
            start_time = time.time()
            for line in f.readlines():
                self.parse_line(line)

            self.logger.debug('completed parsing in %d seconds',
                    time.time() - start_time)

    def parse_line(self, line):
        parsed = ParsedFileLine(line)

        path_parts = parsed.path.path.split('/')
        if path_parts[1] in self.ignored_top: return

        self.paths[parsed.path.path] = parsed.path

        #self.logger.debug('path: %s',parsed.path.path)

    def record(self, flavor):
        self.logger.debug('recording %d paths',len(self.paths))

        start_time = time.time()
        flavor.record('paths', self.paths)
        self.logger.debug('completed recording in %d seconds',
                time.time() - start_time)
