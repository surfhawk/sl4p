# -*- coding: utf-8 -*-
import os
import time
import uuid
import logging
from .utils import purge_old_logfiles, cdprint
from .config import Sl4pConfig
from .getter import get_root_logger
from .getter import get_custom_logger


class sl4p(object):

    @classmethod
    def getLogger(cls, module__file__='', cfg='', tag='', debugprt=0, stats=0, apps_cfgdir='', **kwargs):
        """
        Input parameters are exactly same with Log4py's __init__ method, Please refer that docstring.
        
        :return: configured python's logger object.
        """
        return cls(module__file__, cfg, tag, debugprt, stats, apps_cfgdir, **kwargs).logger

    @classmethod
    def getIndependentLogger(cls, module__file__='', cfg='', indlogger_name='sl4p_ind', debugprt=0):
        if indlogger_name in logging.Logger.manager.loggerDict:
            indlogger_name += '.{}'.format(str(uuid.uuid4())[:4])

        _new_configInst = Sl4pConfig().createInstance(cfg, logger_name=indlogger_name, debugprt=debugprt)

        _new_sl4pInst = cls(module__file__, cfg=_new_configInst, logger_name=indlogger_name)
        if indlogger_name.startswith('sl4p.'):
            _new_sl4pInst.logger.propagate = True

        return _new_sl4pInst.logger

    # TODO: Warning - debugprt 와 stats 항목은, 새로운 context를 열 때(__file__), 기존에 처음열린 context 값으로 초기화 된다.
    def __init__(self, module__file__, cfg='', tag='', debugprt=0, stats=0, apps_cfgdir='', **kwargs):
        """
        Initialize sl4p context.
        
        :param module__file__: __file__ must be passed. This param used to decide logging with root or custom logger.
        :param cfg: <''  or  'your_app_name'  or  'your_sl4p_config.json'  or  your_config_dict: dict>
                         This parameter decides sl4p logger's initial configuring way.
                         There are four ways to configure sl4p logging.
                          - '' (or undefined)  : Initialize logger with default config (built-in).
                                                 Logger will write logfiles to {project_dir}/sl4p_logs dir.
                          - 'your_app_name'  : Initialize logger with 'your_app_name' config as defined key in app_cfg.
                                               (apps config file = /{apps_cfgdir}/apps_cfg.json)
                          - 'your_sl4p_config.json'  : Initialize logger with 'your_sl4p_config.json' config file.
                                                       Assign the config.json's absolute filepath is recommended.
                                                       Also, '.cfg' extension is supported from sl4p-1.4.0 version
                          - your_config_dict <dict>  : Initialize logger with passing python dictionary directly.
                                                       You can override your custom options partially from default cfg.
        :param tag: <str> on with-block style logging, this tag string will recorded to log.
        :param debugprt: <0 or 1> If you want to get some information about initializing logger via cmdline messages,
                                  you can set this debugprt to 1.
        :param stats: <0 or 1 or (1, 'your_stat_file.csv')> Params about doing dimensioning CPU and MEMORY usages.
                                 0 disabled, 1 enabled with default stat_file_name, tuple with custom stat_file defined.
        :param apps_cfgdir: <str> You can specify apps_cfgdir path containing your own 'apps_cfg.json' and
                                  'apps_default.json' to be used for setting up your logger.
                                  Default is {YOUR_OS_HOMEDIR}/sl4p_configs
        """
        self.module__file__ = module__file__
        self.tag = tag

        Sl4pConfig.debugprt = debugprt
        if isinstance(stats, tuple):
            Sl4pConfig.stats_enabled = 1
            Sl4pConfig.stats_file = stats[1]
        else:
            Sl4pConfig.stats_enabled = stats
        if apps_cfgdir:
            if os.path.isdir(apps_cfgdir):
                from .const import _apps_default_cfg_fn, _apps_cfg_fn
                Sl4pConfig.apps_default_cfg_filepath = os.path.join(apps_cfgdir, _apps_default_cfg_fn)
                Sl4pConfig.apps_cfg_filepath = os.path.join(apps_cfgdir, _apps_cfg_fn)
            else:
                cdprint(debugprt, "apps config-dir '{}' does not exist!".format(os.path.abspath(apps_cfgdir)) +
                        "  sl4p will be configured with '$USER_HOME/sl4p_appscfg/apps_*.json'")

        if isinstance(cfg, Sl4pConfig):
            config = cfg
        elif cfg:
            config = Sl4pConfig.instance(cfg)
        else:
            config = Sl4pConfig.instance()

        purge_old_logfiles(config)

        _logger = get_root_logger(config, logger_name=kwargs.get('logger_name', ''))

        if isinstance(config.customConfig.enabled_snippet_dict, dict):
            for snippet in config.customConfig.enabled_snippet_dict.keys():
                if os.path.normpath(snippet) in os.path.normpath(module__file__):
                    _logger = get_custom_logger(config, snippet)
                    break

        self.extras = kwargs
        self.logger = _logger
        # self.logger.debug("@context '%s' with logger '%s'" % (os.path.normpath(module__file__), self.logger.name))

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
