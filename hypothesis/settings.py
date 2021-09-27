import logging
import logging.config

from decouple import config

from hypothesis.commons import get_app_version


class Configuration:
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False

    DB_USER = config('DB_USER')
    DB_PASSWORD = config('DB_PASSWORD')
    DB_HOST = config('DB_HOST', default='0.0.0.0')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/hypothesis'
    )

    # Logging configuration
    LOG_LEVEL = config('LOG_LEVEL', default='INFO', cast=str)
    LOG_VARS = config('LOG_VARS', cast=str).replace("'", '').replace('"', '')
    JSON_LOGS = config('JSON_LOGS', default=False, cast=bool)
    if JSON_LOGS:
        log_format = ' '.join(
            [f'%({variable})' for variable in LOG_VARS.split()]
        )
    else:
        log_format = ''
        for index, variable in enumerate(LOG_VARS.split()):
            if variable != 'asctime':
                log_format += ' '
            log_format += f'%({variable})s'
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'root': {'level': LOG_LEVEL, 'handlers': ['console']},
        'formatters': {
            'default': {'format': log_format, 'datefmt': '%Y-%m-%d.%H:%M:%S'}
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',  # Default is stderr
                'formatter': 'default',
            }
        },
        'loggers': {
            # default for all undefined Python modules
            '': {'level': 'WARNING', 'handlers': ['console']},
            'rose': {
                'level': LOG_LEVEL,
                'handlers': ['console'],
                'propagate': False,
            },
            'celery': {
                'level': LOG_LEVEL,
                'handlers': ['console'],
                'propagate': True,
            },
        },
    }
    if JSON_LOGS:
        LOGGING['formatters']['default'][
            'class'
        ] = 'pythonjsonlogger.jsonlogger.JsonFormatter'

    logging.config.dictConfig(LOGGING)

    VERSION = get_app_version()

    SWAGGER_TEMPLATE = {
        'swagger': '2.0',
        'info': {
            'title': 'hypothesis',
            'description': '''
                This is a minimal financial project written in flask to provide an
                API to handle transactions between customers.
            ''',
            'contact': {
                'responsibleDeveloper': 'Rocky Shimithy',
                'email': 'shimithy@gmail.com',
            },
            'version': VERSION,
        },
        'schemes': ['http', 'https'],
    }
