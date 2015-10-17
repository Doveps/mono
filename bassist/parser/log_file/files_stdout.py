import logging
import time
import re

from . import common
from ...systems import path

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

    # TODO: we will need to get smarter about this
    # a static list of diffs will come back and bite us as soon as we find a
    # system where somebody is retaining important state in /tmp, for example
    ignored = [
            re.compile('^/dev/'),
            re.compile('^/lost+found/'),
            re.compile('^/proc/'),
            re.compile('^/run/'),
            re.compile('^/sys/'),
            re.compile('^/tmp/'),
            re.compile('^/var/log/'),
            ]

    symlink_deref_re = re.compile(r' -> ')

    meta_re = re.compile(r'''
            ^\s* # beginning of line, followed by 0 or more spaces
                (?P<inode>\d{1,20})
            \s+
                (?P<blocks>\d{1,10})
            \s
                (?P<perms>[-cld][-r][-w][-xs][-r][-w][-xs][-r][-w][-xtT])
            \s+
                (?P<lcount>\d{1,10})
            \s
                (?P<owner>[-a-zA-Z0-9_]{1,20})
            \s+
                (?P<group>[-a-zA-Z0-9_]{1,20})
            \s+

                # optional size; char devices don't have this
            (
                (?P<size>\d{1,20})
            \s
            )?

                (?P<month>(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))
            \s+

                # 1 or 2 digits
                (?P<day>\d{1,2})
            \s+

                # valid: 2013 OR 15:58
                (?P<timex>(\d{4}|\d\d:\d\d))
            \s

                # alternate group: symlink has " -> ", other files don't
            (
                (?P<source>.+)\ ->\ (?P<target>.+)
                |
                (?P<path>.+)
            )
            ''', re.VERBOSE)

    def __init__(self, line):
        m = ParsedFileLine.meta_re.match(line)
        try:
            assert m
        except AssertionError, e:
            raise ParsedFileException('Unable to understand line: %s',line)

        p = path.Path()
        p.inode = m.group('inode')
        p.blocks = m.group('blocks')
        p.perms = m.group('perms')
        p.link_count = m.group('lcount')
        p.owner = m.group('owner')
        p.group = m.group('group')
        p.size = m.group('size')
        p.month = m.group('month')
        p.day = m.group('day')
        p.more_time = m.group('timex')

        if p.size is None:
            if p.perms[0] != 'c':
                raise ParsedFileException('Missing file size, but not a char device: %s',line)
        else:
            if p.perms[0] == 'c':
                raise ParsedFileException('Has file size, but is a char device: %s',line)

        self.path = p

        self.ignore = False

        self.set_path(m)

        if self.is_ignored():
            self.ignore = True

    def is_ignored(self):
        for pattern in ParsedFileLine.ignored:
            if pattern.match(self.path.path):
                return True
        return False

    def set_path(self, m):
        '''Set a path and possibly also a symlink target. There's room
        for interpretation here because paths can have spaces, and
        symlinks contain spaces due to their 'foo -> bar' format.'''

        if m.group('path') is not None:

            if self.path.perms[0] == 'l':
                raise ParsedFileException('Invalid symlink format: %s',m.group('path'))

            # ignore "observer effect" commands, that is: Ansible
            if common.Observer.timestamp_re.search(m.group('path')):
                self.ignore = True

            # /opt/VBoxGuestAdditions-4.3.8
            self.path.path = m.group('path').rstrip('\n')
            return

        if self.path.perms[0] != 'l':
            raise ParsedFileException('Symlink formatted path, but file is not a symlink: %s',m.group('path'))

        self.path.path = m.group('source')
        self.path.link_target = m.group('target').rstrip('\n')

        if ParsedFileLine.symlink_deref_re.search(self.path.path):
            raise ParsedFileException('Unexpected symlink dereference found in path: %s',self.path.path)

class FilesStdoutLog(common.Log):

    def parse(self):
        self.logger.debug('parsing')

        self.data = path.Paths()
        self.name = 'paths'

        with open(self.path, 'r') as f:
            start_time = time.time()
            for line in f.readlines():
                self.parse_line(line)

            self.logger.debug('completed parsing in %d seconds',
                    time.time() - start_time)

    def parse_line(self, line):
        parsed = ParsedFileLine(line)

        if parsed.ignore: return

        assert parsed.path.path not in self.data
        self.data[parsed.path.path] = parsed.path

        #self.logger.debug('path: %s',parsed.path.path)
