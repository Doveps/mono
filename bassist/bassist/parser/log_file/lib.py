# Copyright (c) 2015 Kurt Yoder
# See the file LICENSE for copying permission.
import logging
import os
import importlib
import traceback

module_logger = logging.getLogger(__name__)

def get_parser(path):
    '''For a given log file in a path, e.g.
    "/path/to/find_files_stderr.log", look for a log file parsing module
    in the current path. If the parser module is not found, ignore the
    log file.'''

    # ./find_files_stderr.log -> files_stderr
    parser_name = os.path.splitext(os.path.basename(path))[0][5:]
    module_logger.debug('importlib: %s', '..'+parser_name)

    try:
        parser_module = importlib.import_module('..'+parser_name, __name__)
    except ImportError, e:
        if str(e) == 'No module named %s'%parser_name:
            module_logger.debug('no module could be imported for %s; skipping', path)
        else:
            module_logger.warn(
                    'error importing module %s to parse %s; skipping',
                    parser_name, path)
            module_logger.warn('*** traceback:')
            module_logger.warn(traceback.format_exc())
        return None
    except KeyError:
        module_logger.debug('malformed log file %s; skipping', path)
        return None

    # files_stderr -> FileStderrLog
    module_name = ''.join([w.capitalize() for w in parser_name.split('_')]) + 'Log'
    module_logger.debug('module: %s', module_name)

    module_logger.debug('loaded')
    return getattr(parser_module, module_name)(path)
