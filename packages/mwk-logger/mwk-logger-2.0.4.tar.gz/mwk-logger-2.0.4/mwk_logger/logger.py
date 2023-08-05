"""Custom logger with colors on terminal"""
import logging

__version__ = '2.0.4'

# escape codes for changing colors in the terminal
# https://en.wikipedia.org/wiki/ANSI_escape_code
ESC = dict(
    DEFAULT='\x1b[39m',
    NORMAL='\x1b[37m',
    GRAY='\x1b[90m',
    WHITE='\x1b[97m',
    GREEN='\x1b[92m',
    YELLOW='\x1b[93m',
    DRED='\x1b[31m',
    RED='\x1b[91m',
    CRITICAL='\x1b[30;1;101m',
    RESET='\x1b[0m')

# formats for components of the log record
FMT = dict(
    LEVEL=r'[%(levelname)8s]',
    TIME=r'%(asctime)s',
    INFO=r'[%(name)s] %(module)s.%(funcName)s%(lineno)4s',
    MSG=r'%(message)s')

# general date/time format
DATE_FMT = r'%y.%m.%d %H:%M'

# record definition for logging in file
FILE_FMT = ' '.join([fmt for fmt in FMT.values()])


class MwkFormatter(logging.Formatter):
    """Custom formatter class"""

    def get_color_fmt(self, general_color, info_color):
        """Get coloured format of record for logging in terminal.
        It uses format components and given colors.
        <general_color> is for level and message, <info_color> is for time and info part of the record.
        Returns logging record format."""
        time_fmt = FMT['TIME'] if self.time else ''
        return general_color + FMT['LEVEL'] +\
               info_color + ' ' + time_fmt + FMT['INFO'] + ' ' +\
               general_color + FMT['MSG'] + ESC['RESET']

    def __init__(self, time):
        """Defining formats of logging levels and date/time format for custom logger."""
        super().__init__()
        self.date_fmt = DATE_FMT
        self.time = time
        self.FORMATS = {logging.DEBUG   : self.get_color_fmt(ESC['NORMAL'], ESC['GRAY']),
                        logging.INFO    : self.get_color_fmt(ESC['WHITE'], ESC['NORMAL']),
                        logging.WARNING : self.get_color_fmt(ESC['YELLOW'], ESC['NORMAL']),
                        logging.ERROR   : self.get_color_fmt(ESC['RED'], ESC['DRED']),
                        logging.CRITICAL: self.get_color_fmt(ESC['CRITICAL'], ESC['RESET'] + ESC['WHITE'])}

    def format(self, record):
        """Function needed for logging record generation according to defined formats."""
        log_fmt = self.FORMATS.get(record.levelno)
        log_date_fmt = self.date_fmt
        formatter = logging.Formatter(log_fmt, log_date_fmt)
        return formatter.format(record)


class LoggerCreationError(Exception):
    """Custom error raised when creating logger failed"""


class LogHandler:
    """Class for setting up loger handler."""

    def __init__(self, _handler, _level, _formatter):
        self.handler = _handler
        self.handler.setLevel(_level)
        self.handler.setFormatter(_formatter)


class MwkLogger:
    """Custom logger class"""
    def __new__(cls,
                name='mwk',                # name of the logger
                file='mwk.log',            # path to log file
                stream_level='WARNING',    # logging to terminal level
                file_level=None,           # logging to file level
                time=False):               # add timestamp to stream logging
        """Constructor parameters:
        name - name of the logger, by default = 'mwk',
        file - path to file to log into, by default = 'mwk.log',
        stream_level - logging level for terminal, by default = 'WARNING',
        file_level - logging level for file, by default = None,
        time - if timestamp should be added to terminal log, by default = False,

        LEVELS:
         None - no logging or:
         'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'.
        If both levels are set to None stream_level is changed to WARNING.

        !!! __new__ returns instance of logging.logger, no need to use .logger after the constructor """
        try:
            logger = logging.getLogger(name)


            logger.setLevel('DEBUG')
            # if both levels set to None then set stream level to DEBUG
            if not stream_level and not file_level:
                stream_level = 'DEBUG'
            # set logger handlers according to settings
            if stream_level:  # for terminal
                stream = LogHandler(logging.StreamHandler(),
                                    stream_level,
                                    MwkFormatter(time))
                logger.addHandler(stream.handler)
            if file_level:  # and for file
                file = LogHandler(logging.FileHandler(file),
                                  file_level,
                                  logging.Formatter(fmt=FILE_FMT, datefmt=DATE_FMT))
                logger.addHandler(file.handler)
            return logger
        # catch error creating handler
        except Exception as err:
            raise LoggerCreationError('ERROR creating logger:') from err


if __name__ == '__main__':
    class TestError(Exception):
        pass


    # Record format
    print('Record format:', FILE_FMT)
    # Test colors
    [print(''.join([c, n]), end=' ') for n, c in ESC.items()]
    print()

    # Testing custom logger
    # new logger referred by variable: log
    # !!! v2.0.0 no need to use .logger after the constructor !!!
    log = MwkLogger(name='mwk',
                    file='logger.log',
                    stream_level='DEBUG',
                    file_level='DEBUG',
                    time=False)
    # some log records...
    log.debug('This is a debug message.')
    log.info('This is an info message.')
    log.warning('This is a warning message.')
    log.error('This is an error message!')
    log.critical('This is a critical message!!!')
    try:
        raise TestError('Same like log.error but logs also traceback when error was raised!')
    except Exception:
        log.exception('This is an exception message!')
