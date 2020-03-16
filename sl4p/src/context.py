# -*- coding: utf-8 -*-
import os
import time
import uuid
from .utils import purge_old_logfiles
from .config import Sl4pConfig
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
        Initialize sl4p context.
        
        :param module__file__: __file__ must be passed. This param used to decide logging with root or custom logger.
        :param cfg_param: <''  or  'your_app_name'  or  'your_sl4p_config.json'  or  your_config_dict: dict>
                         This parameter decides sl4p logger's initial configuring way.
                         There are four ways to configure sl4p logging.
                          - '' (or undefined)  : Initialize logger with default config (built-in).
                                                 Logger will write logfiles to {project_dir}/sl4p_logs dir.
                          - 'your_app_name'  : Initialize logger with 'your_app_name' config as defined key in app_cfg.
                                               (apps config file = /opt/zl/nwi/bin/sl4p/mconfigs/apps_cfg.json)
                                               It works only TODO
                          - 'your_sl4p_config.json'  : Initialize logger with 'your_sl4p_config.json' config file.
                                                       Assign the config.json's absolute filepath is recommended.
                          - your_config_dict <dict>  : Initialize logger with passing python dictionary directly.
                                                       You can override your custom options partially from default cfg.
        :param tag: <str> on with-block style logging, this tag string will recorded to log.
        :param debugprt: <0 or 1> If you want to get some information about initializing logger via cmdline messages,
                                  you can set this debugprt to 1.
        :param stats: <0 or 1 or (1, 'your_stat_file.csv')> Params about doing dimensioning CPU and MEMORY usages.
                                 0 disabled, 1 enabled with default stat_file_name, tuple with custom stat_file defined.
        :param kwargs:  (NotImplemented yet)
        """
        self.module__file__ = module__file__
        self.tag = tag
        
        Sl4pConfig.debugprt = debugprt
        if isinstance(stats, tuple):
            Sl4pConfig.stats_enabled = 1
            Sl4pConfig.stats_file = stats[1]
        else:
            Sl4pConfig.stats_enabled = stats
        
        if cfg_param:
            config = Sl4pConfig.instance(cfg_param)
        else:
            config = Sl4pConfig.instance()
        
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