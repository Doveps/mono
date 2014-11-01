import imp
import os

from . import common

def get_from_name(path):
    # ./find_files_stderr.log -> files_stderr
    log_name = os.path.splitext(os.path.basename(path))[0][5:]

    # files_stderr -> /this/module/path/files_stderr.py
    module_file = os.path.join(os.path.dirname(__file__), '%s.py'%log_name)
    try:
        python_module = imp.load_source(log_name, module_file)
    except FileNotFoundError:
        return None

    # files_stderr -> FileStderrLog
    camel_cased_log = ''.join([w.capitalize() for w in log_name.split('_')]) + 'Log'
    if not hasattr(python_module, camel_cased_log):
        return None

    return getattr(python_module, camel_cased_log)(path)
