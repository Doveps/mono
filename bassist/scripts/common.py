# Copyright (c) 2015 Kurt Yoder
# See the file LICENSE for copying permission.
# This object is intended to run from script bassist.py
import logging
import logging.config
import ConfigParser

class Script(object):
    '''This module contains things that are available for use of our packages'
    scripts. This includes setting up logger, etc.'''

    def set_logging(self):
        '''If we're running from the root of the project, this stuff will work.
        If not, load logging_config.'''

        try:
            logging.config.fileConfig('log.conf', disable_existing_loggers=False)
        except ConfigParser.NoSectionError:
            # probably no log.conf file
            logging.basicConfig(
                    format='%(message)s',
                    )

        self.logger = logging.getLogger(__name__)

        try:
            from log_override import LOG_OVERRIDES
            logging.config.dictConfig(LOG_OVERRIDES)
        except:
            self.logger.debug('unable to load log_override; ignoring')

    def finish(self):
        pass
