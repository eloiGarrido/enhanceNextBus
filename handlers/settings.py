import logging.config
import os

LOGGING_CONFIG = None

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, "log/nextBus.log"),
            'formatter': 'simple',
        },
    },
    'loggers': {
        'nextBus': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
            'formatter': 'simple',
        },
    },
}


logging.config.dictConfig(LOGGING)
WEB_ENDPOINT = 'http://webservices.nextbus.com/service/publicXMLFeed?'