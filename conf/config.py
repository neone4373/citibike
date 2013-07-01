# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import logging
import datetime


def globalLogger(level, handle=""):
    '''
    Make a global logging object.
    '''
    global logger
    #print __f__
    logger = logging.getLogger("logger")
    #logger.info(logger.handlers)
    #logger.info(handle)
    if not logger.handlers:
        logger.setLevel(level)
        if handle == "":
            h = logging.StreamHandler()
        else:
            h = logging.FileHandler(handle)
        f = logging.Formatter("%(levelname)s %(asctime)s %(funcName)s %(lineno)d %(message)s")
        h.setFormatter(f)
        logger.addHandler(h)
    #logger.info(logger.handlers)
    return logger


class Timeit(object):
    """Timeit decorator in addition to running the function times how long it takes and prints it to the log"""
    def __init__(self, mod=1):
        # super(Timeit, self).__init__()
        # self.func = func
        self.mod = mod

    def __call__(self, func):
        def wrapped_func(*arg, **kwargs):
            start_time = datetime.datetime.now()
            wrapped_func.called += 1
            #print wrapped_func.called, self.mod, wrapped_func.called % self.mod
            output = func(*arg, **kwargs)
            end_time = datetime.datetime.now()
            time_to_run = end_time - start_time
            wrapped_func.seconds_run += time_to_run
            runtime_tuple = divmod(wrapped_func.seconds_run.days * 86400 + wrapped_func.seconds_run.seconds + round(wrapped_func.seconds_run.microseconds/1000000., 3), 60)
            if wrapped_func.called % self.mod == 0:
                logger.debug("Runtime in %s after %s calls:  %s:%s" % (func.__name__, wrapped_func.called, int(runtime_tuple[0]), runtime_tuple[1]))
                # wrapped_func.seconds_run = datetime.timedelta(0)
            return output
        wrapped_func.called = 0
        wrapped_func.seconds_run = datetime.timedelta(0)
        return wrapped_func
