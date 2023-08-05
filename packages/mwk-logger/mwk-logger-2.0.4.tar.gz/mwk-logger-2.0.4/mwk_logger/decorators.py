import logging
from functools import wraps, partial
from time import perf_counter_ns as pc
from inspect import signature
from mwk_logger.logger import ESC


class BadLoggerError(Exception):
    pass


def color_msg(info, func, result):
    return ''.join([ESC['GREEN'], info, ESC['NORMAL'], func, ESC['GREEN'], result, ESC['RESET']])


def log_msg(info, func, result):
    return ''.join([info, func, result])


def output(info, func, result, logger):
    if logger:
        logger.info(log_msg(info, func, result))
    else:
        print(color_msg(info, func, result))


def time_formatter(ns):
    s = ns * 1e-9
    secs = s // 1
    ms = (s % 1) * 1000
    msecs = ms // 1
    usecs = (ms % 1) * 1000 // 1
    return f'{secs:.0f} sec(s) {msecs:.0f} msec(s) {usecs:.0f} usec(s)'


def timer(func=None, *, logger=None):
    """Print the runtime of the decorated function"""
    if logger and not isinstance(logger, logging.Logger):
        raise BadLoggerError('Instance of logger should be passed to timer.')
    if func is None:
        return partial(timer, logger=logger)

    @wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = pc()
        value = func(*args, **kwargs)
        end_time = pc()
        i = f'[Timer   ]'
        f = f' {func.__module__}.{func.__name__}: '
        r = time_formatter(end_time - start_time)
        output(i, f, r, logger)
        return value
    return wrapper_timer


def f_sig(func=None, *, logger=None):
    """Print the function signature and return value"""
    if logger and not isinstance(logger, logging.Logger):
        raise BadLoggerError('Instance of logger should be passed to f_sig.')
    if func is None:
        return partial(f_sig, logger=logger)

    @wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f'{k}={v!r}' for k, v in kwargs.items()]
        arguments = ', '.join(args_repr + kwargs_repr)
        sig = str((signature(func)))
        i = f'[Call    ]'
        f = f' {func.__module__}.{func.__name__}{sig}'
        r = f'({arguments})'
        output(i, f, r, logger)
        value = func(*args, **kwargs)
        i = f'[Return  ]'
        f = f' {func.__module__}.{func.__name__}({arguments}) = '
        r = f'{value!r}'
        output(i, f, r, logger)
        return value
    return wrapper_debug


if __name__ == '__main__':
    # Testing decorators
    from time import sleep
    from logger import MwkLogger

    @timer
    @f_sig
    def functionA(*args, **kwargs):
        # ... some function ...
        sleep(1.531)
        return True

    x = functionA('arg', kwarg='kwarg')

    log = MwkLogger(stream_level='DEBUG', file_level='DEBUG')

    @timer(logger=log)
    @f_sig(logger=log)
    def functionB(*args, **kwargs):
        # ... some function to be logged...
        sleep(1.135)
        return True

    y = functionB('arg', kwarg='kwarg')
