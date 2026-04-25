import logging
import logging.config

class MqttLogger:
    def __init__(self, name : str) -> None:
        self.loggerType = name
        self.loggingConfig = { 
            'version': 1,
            'disable_existing_loggers': True,
            'formatters': { 
                'standard': { 
                    'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
                },
            },
            'handlers': { 
                'default': { 
                    'level': 'DEBUG',
                    'formatter': 'standard',
                    'class': 'logging.StreamHandler',
                    'stream': 'ext://sys.stdout',  # Default is stderr
                },
            },
            'loggers': { 
                'console_logger': {  # root logger
                    'handlers': ['default'],
                    'level': 'DEBUG',
                    'propagate': False
                }
            } 
        }
    
    
    def getLogger(self) -> logging.Logger:
        logging.config.dictConfig(self.loggingConfig)
        return logging.getLogger(self.loggerType)
