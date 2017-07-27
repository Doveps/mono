# Copy/rename this file to "log_override.py" in order to change logging
# behaviour. Below is an example which reduces the amount of logging from
# "parser.host".
LOG_OVERRIDES = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'parser.host': {
            'level': 'WARN',
            'propagate': False
        },
    }
}
