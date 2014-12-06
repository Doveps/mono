import logging
import shlex

from . import common
from systems import os_file

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

        # sacrifice a bit of name clarity to reduce a lot of repetition
        self.of = os_file.File()

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
        (self.of.inode, self.of.blocks, self.of.perms,
                self.of.link_count, self.of.owner, self.of.group,
                self.of.month, self.of.day, self.of.more_time,
                self.of.path) = self.parts[0:10]

    def set_fields_before_path(self):
        '''Set fields up to a path:
         523431    4 drwxr-xr-x   9 root     root         4096 Apr 19  2014
        '''
        (self.of.inode, self.of.blocks, self.of.perms,
                self.of.link_count, self.of.owner, self.of.group,
                self.of.size, self.of.month, self.of.day,
                self.of.more_time) = self.parts[0:10]

    def set_path(self, path_parts):
        '''Set a path and possibly also a symlink target. There's room
        for interpretation here because paths can have spaces, and
        symlinks contain spaces due to their 'foo -> bar' format.'''

        count = len(path_parts)
        if count == 1:
            # /opt/VBoxGuestAdditions-4.3.8
            self.of.path = path_parts[0]
            return

        if count == 3:
            if path_parts[1] == '->':
                # /bin/dnsdomainname -> hostname
                self.of.path = path_parts[0]
                self.of.link_target = path_parts[2]
                return

        raise ParsedFileException('Unable to understand path: %s',self.parts)

class FilesStdoutLog(common.Log):
    ignored_top = [ 'dev', 'lost+found', 'proc', 'run', 'sys', 'tmp' ]
    # ignore more?
    #  /home/*/.ansible
    #  /var/log/*

    def parse(self):
        self.logger.debug('parsing')

        self.files = {}
        with open(self.path, 'r') as f:
            for line in f.readlines():
                self.parse_line(line)

    def parse_line(self, line):
        parsed = ParsedFileLine(line)

        path_parts = parsed.of.path.split('/')
        if path_parts[1] in self.ignored_top: return

        self.files[parsed.of.path] = parsed.of

        #self.logger.debug('path: %s',parsed.of.path)

    def record(self, flavor):
        self.logger.debug('recording %d files',len(self.files))
        flavor.record('files', self.files)
