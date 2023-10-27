import logging

# output print or logging
GLOABLE_OUTPUT_PRINT = True

class Logger:
    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            log_level = logging.DEBUG
            cls._instance.__init_manual__(log_level)
        return cls._instance

    @classmethod
    def debug(cls, message, *args):
        cls.instance()._debug(message, *args)

    @classmethod
    def info(cls, message, *args):
        cls.instance()._info(message, *args)

    @classmethod
    def warning(cls, message, *args):
        cls.instance()._warning(message, *args)

    @classmethod
    def error(cls, message, *args):
        cls.instance()._error(message, *args)

    @classmethod
    def critical(cls, message, *args):
        cls.instance()._critical(message, *args)

    def __init_manual__(self, log_level=logging.DEBUG):
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s [%(levelname)s] - %(message)s',
        )
        self.logger = logging.getLogger('Face_logger')
        self.log_level_dict = {
            10: 'Debug',
            20: 'Info',
            30: 'Warning',
            40: 'Error',
            50: 'Critical'
        }

    def _debug(self, message, *args):
        self._log(logging.DEBUG, message, *args)

    def _info(self, message, *args):
        self._log(logging.INFO, message, *args)

    def _warning(self, message, *args):
        self._log(logging.WARNING, message, *args)

    def _error(self, message, *args):
        self._log(logging.ERROR, message, *args)

    def _critical(self, message, *args):
        self._log(logging.CRITICAL, message, *args)

    def _log(self, log_level, message, *args):
        log_message = message
        if args:
            log_message += ', ' + ', '.join(map(str, args))
        
        log_message += '\n'
        global GLOABLE_OUTPUT_PRINT
        if not GLOABLE_OUTPUT_PRINT:
            self.logger.log(log_level, log_message)
        else:
            print(f"{self.log_level_dict[log_level]}: {log_message}")