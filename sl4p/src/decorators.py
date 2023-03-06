from functools import wraps
import sys
import os
import time
import uuid
from .context import sl4p
# import traceback
# import inspect

def sl4p_try(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        frame = sys._getframe().f_back
        __func_file = os.path.abspath(frame.f_code.co_filename)
        # performance : https://gist.github.com/JettJones/c236494013f22723c1822126df944b12
        
        logger = sl4p.getLogger(__func_file)

        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(e)
            euuid = str(uuid.uuid4())[:5]
            logger.debug("Exception occurred on f`{}() ----- (&{})  args, kwargs ::".format(func.__name__, euuid))
            for _i, _arg in enumerate(args):
                logger.debug("   (&{}) - a[{}]= {}. {}".format(euuid, _i, type(args[_i]), args[_i]))
            for _i, _k in enumerate(kwargs):
                _v = kwargs.get(_k)
                logger.debug("   (&{})-- k[{}] '{}': {}. {}".format(euuid, _i, _k, type(_v), _v))
            logger.error("@sl4p_try catches exception '{}' (&{}).  omit the remaining and do on ...".format(e, euuid))

    return wrapped


# TODO: is there any way to remove the parts that overlaps with sl4p_try?
def sl4p_try_exit(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        frame = sys._getframe().f_back
        __func_file = os.path.abspath(frame.f_code.co_filename)
        # performance : https://gist.github.com/JettJones/c236494013f22723c1822126df944b12

        logger = sl4p.getLogger(__func_file)

        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(e)
            euuid = str(uuid.uuid4())[:5]
            logger.debug("Exception occurred on f`{}() ----- (&{})  args, kwargs ::".format(func.__name__, euuid))
            for _i, _arg in enumerate(args):
                logger.debug("   (&{}) - a[{}]= {}. {}".format(euuid, _i, type(args[_i]), args[_i]))
            for _i, _k in enumerate(kwargs):
                _v = kwargs.get(_k)
                logger.debug("   (&{})-- k[{}] '{}': {}. {}".format(euuid, _i, _k, type(_v), _v))
            logger.error("@sl4p_try_exit catches exception '{}' (&{}).  Exit program ...".format(e, euuid))
            exit()

    return wrapped


class sl4p_time(object):
    def __init__(self, tag='', log_level='debug'):
        self.tag = tag
        self.log_level = log_level.lower()
        self.b_uuid = str(uuid.uuid4())[:8]
        
    def __call__(self, func):
        
        @wraps(func)
        def wrapped(*args, **kwargs):
            frame = sys._getframe().f_back
            __func_file = os.path.abspath(frame.f_code.co_filename)
            callf_basename = os.path.basename(__func_file)
            func_name = func.__name__
            logger = sl4p.getLogger(__func_file)
            logging_func = getattr(logger, self.log_level)
            
            st_t = time.time()
            logging_func("%s f`%s() %s@%s started" % (callf_basename, func_name,
                                                      "#{} ".format(self.tag) if self.tag else '',
                                                      self.b_uuid))
            _return = func(*args, **kwargs)
            end_t = time.time()
            logging_func("%s f`%s %s@%s finished  ----  Elapsed  %8.4f s\n" % (callf_basename, func_name,
                                                                            "#{} ".format(self.tag) if self.tag else '',
                                                                            self.b_uuid, end_t - st_t))
            
            return _return
        
        return wrapped
