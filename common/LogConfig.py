import logging.config
import os

from tornado.options import options


LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False, # 是否禁止已经存在的日志器
    'formatters': {
        'simple': {
            'format': '[%(levelname)s] [%(asctime)s] [%(pathname)s %(module)s %(funcName)s %(lineno)d] message: %(message)s'
        },
        'verbose': {
            'format': '[%(levelname)s] %(asctime)s %(module)s %(lineno)d %(message)s'
        }
    },

    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'myapp': {  # 向文件中输出日志
            'level': 'INFO',
            # 'class': 'logging.handlers.RotatingFileHandler',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(options.logbase+"-info.log"),  # 日志文件的位置
            'backupCount': 0,
            'interval': 1,
            'when': 'D',
            'formatter': 'simple'
        },
        'error': {  # 向文件中输出日志
            'level': 'ERROR',
            # 'class': 'logging.handlers.RotatingFileHandler',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename':  os.path.join(options.logbase+ "-error.log"),  # 日志文件的位置
            'backupCount': 0,
            'interval': 1,
            'when': 'D',
            'formatter': 'simple'
        },
        'warn': {  # 向文件中输出日志
            'level': 'WARN',
            # 'class': 'logging.handlers.RotatingFileHandler',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(options.logbase+"-warn.log"),  # 日志文件的位置
            'backupCount': 0,
            'interval': 1,
            'when': 'D',
            'formatter': 'simple'
        },
    },
    'loggers': {  # 日志器
        'myapp': {  # 定义了一个名为myapp的日志器
            'handlers': ['myapp','error','warn'],  # 可以同时向终端与文件中输出日志
            'level': 'INFO',  # 日志器接收的最低日志级别
            'propagate': True,  # 是否继续传递日志信息
        }
    }
}

logging.config.dictConfig(LOG_CONFIG)