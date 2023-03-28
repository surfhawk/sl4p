# -*- coding: utf-8 -*-
import sys
import os
import atexit
import traceback
import time
import uuid
import logging
from .getter import get_root_logger
from .stats_performance import stat_start, stat_stop

post_except_terminationf_list = []


def _run_post_except_terminations(eh):
    exc_info = None
    func = None
    while post_except_terminationf_list:
        func, args, kargs = post_except_terminationf_list.pop()
        try:
            eh.logger.info("run post_except_termination_f`{}(), args-{}, kwargs-{}".format(func.__name__, str(args),
                                                                                           str(kargs)))

            func(*args, **kargs)
            eh.logger.info("Program  @%s  post except termination '%s' finished!" % (eh.b_uuid, func.__name__))
        except:
            exc_info = sys.exc_info()

    if exc_info is not None:
        eh.logger.critical("Unexpected critical exception occurred on '%s'." % (func.__name__), exc_info=exc_info)
        eh.logger.critical("Program  @%s  post except termination failed." % (eh.b_uuid))

    EmbeddingHandler.end_t = time.time()
    eh.logger.info("Program  @%s  exception-exited.  <<%s>>  -----  Elapsed  %8.4f s\n" % (eh.b_uuid, eh.argv0_bn,
                                                                                           eh.end_t - eh.st_t))


def register_post_exception_terminationf(func, *f_args, **f_kargs):
    post_except_terminationf_list.append((func, f_args, f_kargs))
    return func


# https://stackoverflow.com/questions/9741351/how-to-find-exit-code-or-reason-when-atexit-callback-is-called-in-python
# TODO: Check with origin code...
class EmbeddingHandler(object):
    exitHandler = None
    logger = None
    stat_res_process = None

    st_t = None
    end_t = None
    b_uuid = None

    sl4pConfig = None
    argv0_bn = ''

    def __init__(self):
        self.exc_value = None

    def exc_handler(self, exc_type, exc_value, traceback, *args):
        self.exc_type = exc_type
        self.exc_value = exc_value
        self.tb = traceback

    def exit(self, code=0):
        self._orig_exit(code)

    def hook(self):
        self._orig_exit = sys.exit
        sys.exit = self.exit
        sys.excepthook = self.exc_handler

    @classmethod
    def register_embedding(cls, l4ppConfig):
        cls.sl4pConfig = l4ppConfig
        cls.argv0_bn = os.path.basename(sys.argv[0])
        cls.exitHandler = EmbeddingHandler()
        cls.exitHandler.hook()

        cls.logger = get_root_logger(cls.sl4pConfig)

        EmbeddingHandler.b_uuid = str(uuid.uuid4())[:8]
        EmbeddingHandler.st_t = time.time()
        tz_H = - time.timezone // 3600
        tz_M = (- time.timezone // 60) % 60

        if cls.sl4pConfig.stats_enabled:
            stat_start(cls.sl4pConfig)

        cls.logger.info("OPERATING TIMEZONE: {:+d}:{:02d}".format(tz_H, tz_M))
        cls.logger.info("Program  @{}  started.  <<{}>>".format(EmbeddingHandler.b_uuid, cls.argv0_bn))
        cls.logger.debug("         @@-- argv[0] = {}".format(sys.argv[0]))
        atexit.register(EmbeddingHandler.finalize_process)

    @classmethod
    def finalize_process(cls):
        eh = cls.exitHandler
        if cls.exitHandler is None:
            pass
        elif cls.exitHandler.exc_value is not None:
            # traceback.print_tb(cls.exitHandler.tb)  # console print
            cls.logger.critical("Unexpected exception occurred!! = {}, Program  @{}  checks post_except_terminations .." \
                                .format(str(cls.exitHandler.exc_type), cls.b_uuid),
                                exc_info=(eh.exc_type, eh.exc_value, eh.tb))
            if post_except_terminationf_list:
                _run_post_except_terminations(cls)
        else:
            EmbeddingHandler.end_t = time.time()
            cls.logger.info("Program  %s  finished  <<%s>>  -----  Elapsed  %8.4f s\n" % (cls.b_uuid, cls.argv0_bn,
                                                                                          cls.end_t - cls.st_t))
        stat_stop()
        logging.shutdown()
