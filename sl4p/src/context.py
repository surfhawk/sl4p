# -*- coding: utf-8 -*-
import os
import time
import uuid
from .utils import purge_old_logfiles
from .config import L4ppConfig
from .getter import get_root_logger
from .getter import get_custom_logger

class sl4p(object):
    
    @classmethod
    def getLogger(cls, module__file__, cfg_param='', tag='', debugprt=0, stats=0, **kwargs):
        """
        Input parameters are exactly same with Log4py's __init__ method, Please refer that docstring.
        
        :return: configured python's logger object.
        """
        return cls(module__file__, cfg_param, tag, debugprt, stats, **kwargs).logger
    
    # TODO: Warning - debugprt 와 stats 항복은, 새로운 context를 열 때(__file__), default value 값으로 초기화 된다.
    def __init__(self, module__file__, cfg_param='', tag='', debugprt=0, stats=0, **kwargs):
        """
        Initialize Log4py Context.
        
        :param module__file__:
        :param cfg_param:
        :param tag:
        :param debugprt:
        :param stats: 
        :param kwargs:
        """
        self.module__file__ = module__file__
        self.tag = tag
        
        L4ppConfig.debugprt = debugprt
        if isinstance(stats, tuple):
            L4ppConfig.stats_enabled = 1
            L4ppConfig.stats_file = stats[1]
        else:
            L4ppConfig.stats_enabled = stats
        
        if cfg_param:
            config = L4ppConfig.instance(cfg_param)
        else:
            config = L4ppConfig.instance()
        
        purge_old_logfiles(config)
        
        _logger = get_root_logger(config)
        
        if isinstance(config.customConfig.enabled_snippet_dict, dict):
            for snippet in config.customConfig.enabled_snippet_dict.keys():
                if os.path.normpath(snippet) in os.path.normpath(module__file__):
                    _logger = get_custom_logger(config, snippet)
                    break
        
        self.extras = kwargs
        self.logger = _logger
        #self.logger.debug("@context '%s' with logger '%s'" % (os.path.normpath(module__file__), self.logger.name))
    
    def __enter__(self):
        self.callf_basename = os.path.basename(self.module__file__)
        self.b_uuid = str(uuid.uuid4())[:8]
        self.st_t = time.time()
        self.logger.debug("%s %s@%s started" % (self.callf_basename, 
                                                "#{} ".format(self.tag) if self.tag else '',
                                                self.b_uuid))
        return self.logger
    
    def __exit__(self, exc_type, ex_value, ex_trackback):
        self.end_t = time.time()
        self.logger.debug("%s %s@%s finished  ----  Elapsed %8.4f s" % (self.callf_basename,
                                                                        "#{} ".format(self.tag) if self.tag else '',
                                                                        self.b_uuid,
                                                                        self.end_t - self.st_t))