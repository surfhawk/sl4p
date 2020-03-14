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
    
    return wrapped


class sl4p_time(object):
    def __init__(self, tag=''):
        self.tag = tag
        self.b_uuid = str(uuid.uuid4())[:8]
        
    def __call__(self, func):
        
        @wraps(func)
        def wrapped(*args, **kwargs):
            frame = sys._getframe().f_back
            __func_file = os.path.abspath(frame.f_code.co_filename)
            callf_basename = os.path.basename(__func_file)
            func_name = func.__name__
            logger = sl4p.getLogger(__func_file)
            
            st_t = time.time()
            logger.debug("%s f`%s() %s@%s started" % (callf_basename, func_name,
                                                      "#{} ".format(self.tag) if self.tag else '',
                                                      self.b_uuid))
            _return = func(*args, **kwargs)
            end_t = time.time()
            logger.debug("%s f`%s %s@%s finished  ----  Elapsed  %8.4f s" % (callf_basename, func_name,
                                                                             "#{} ".format(self.tag) if self.tag else '',
                                                                             self.b_uuid,
                                                                             end_t - st_t))
            
            return _return
        
        return wrapped