"""
Logging configurations

Logging Levels (Only events of selected level or higher recorded)

CRITICAL 50
ERROR    40
WARNING  30
INFO     20
DEBUG    10
NOTSET    0
"""
from pydantic import BaseModel


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    INFO_FILE_PATH = "info.log"
    ERROR_FILE_PATH = "error.log"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        'info': {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s | %(asctime)s | %(name)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        'error': {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": '%(levelprefix)s | %(asctime)s | %(name)s | %(process)d::%(module)s|%(lineno)s:: %(message)s',
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        'debug_console_handler': {
            'level': 'DEBUG',
            'formatter': 'info',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'info_rotating_file_handler': {
            'level': 'INFO',
            'formatter': 'info',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': INFO_FILE_PATH,
            'mode': 'a',
            'maxBytes': 1048576,
            'backupCount': 10
        },
        'warning_file_handler': {
            'level': 'WARNING',
            'formatter': 'info',
            'class': 'logging.FileHandler',
            'filename': ERROR_FILE_PATH,
            'mode': 'a',
        },
        'error_file_handler': {
            'level': 'ERROR',
            'formatter': 'error',
            'class': 'logging.FileHandler',
            'filename': ERROR_FILE_PATH,
            'mode': 'a',
        },
        'critical_mail_handler': {
            'level': 'CRITICAL',
            'formatter': 'error',
            'class': 'logging.handlers.SMTPHandler',
            'mailhost' : 'localhost',
            'fromaddr': 'monitoring@domain.com',
            'toaddrs': ['dev@domain.com', 'qa@domain.com'],
            'subject': 'Critical error with application name'
        },
    }
    loggers = {
        '': {  # root logger
            'level': 'NOTSET',
            'handlers': ['debug_console_handler', 'info_rotating_file_handler', 'error_file_handler', 'critical_mail_handler'],
        },
        'log_summarizer': {
            'level': 'INFO',
            'propagate': False,
            'handlers': ['debug_console_handler', 'info_rotating_file_handler', 'error_file_handler'],
        },
    }
