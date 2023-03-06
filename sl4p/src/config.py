# -*- coding: utf-8 -*-
import json
import os
import sys
from imp import reload
from .utils import cdprint, override_dict, replace_dict_key
from .const import _apps_default_config_filepath, _apps_config_filepath, _default_encoding
from .const import _config_version_key, _V_default_config_version, _V_apps_config_version
from .embedding import EmbeddingHandler


class AttributeDict(dict): 
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    

class Sl4pConfig(object):
    __instance = None
    debugprt = 0
    stats_enabled = 0
    stats_file = ''
    
    mconfig_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'mconfigs')
    
    file_default_cfg_filepath = os.path.join(mconfig_dir, 'cfgf_default.json')
    
    apps_default_cfg_filepath = _apps_default_config_filepath
    apps_cfg_filepath = _apps_config_filepath
    
    def load_json_as_dict(cls, cfg_filepath):
        config_str = open(cfg_filepath).read()
        config = json.loads(config_str)
        return config
    
    def load(self, cfg_param='', debugprt=0):
        config = None
        
        if cfg_param:
            if isinstance(cfg_param, dict):  # DICT CONFIG
                cdprint(debugprt, "Initialize sl4p Logging with dictionary= {}".format(cfg_param))
                file_default_config = self.load_json_as_dict(Sl4pConfig.file_default_cfg_filepath)
                config = override_dict(file_default_config, cfg_param)

            elif os.path.isfile(cfg_param) and (os.path.splitext(cfg_param)[1] == '.json' or
                    os.path.splitext(cfg_param)[1] == '.logcfg'):  # FILE CONFIG
                cdprint(debugprt, "Initialize sl4p Logging with configfile= {}".format(cfg_param))
                file_default_config = self.load_json_as_dict(Sl4pConfig.file_default_cfg_filepath)
                file_config = self.load_json_as_dict(cfg_param)
                if _V_default_config_version != file_config.get(_config_version_key, ''):
                    cdprint(1, ("\nWARNING :: Input config version ({}) is different from " +
                               "the sl4p library's standard config version ({}).").format(
                        file_config.get(_config_version_key, ''), _V_default_config_version
                    ) + "\n        :: " +
                    "Please migrate your config. Otherwise some functions may not work or may malfunction.\n")

                # Migration sl4p<=1.3.x  to  1.4.0+
                for _cfg in [file_default_config, file_config]:
                    replace_dict_key(_cfg, old_key='DEFAULT', new_key='LOG')
                    replace_dict_key(_cfg, old_key='CUSTOM_LOG', new_key='SNIPPET_LOG')

                config = override_dict(file_default_config, file_config)

            else:   # APP CONFIG
                cdprint(debugprt, "Initialize sl4p Logging with app config '{}'".format(cfg_param))
                cdprint(debugprt, "Exist apps_default_cfg_file={} : {}".format(Sl4pConfig.apps_default_cfg_filepath,
                                                                          os.path.exists(Sl4pConfig.apps_default_cfg_filepath)))
                if not os.path.exists(Sl4pConfig.apps_default_cfg_filepath):
                    Sl4pConfig.apps_default_cfg_filepath = os.path.join(Sl4pConfig.mconfig_dir, 'apps_default.json')

                cdprint(debugprt, "Exist apps_cfg_file={} : {}".format(Sl4pConfig.apps_cfg_filepath,
                                                                  os.path.exists(Sl4pConfig.apps_cfg_filepath)))
                if not os.path.exists(Sl4pConfig.apps_cfg_filepath):
                    Sl4pConfig.apps_cfg_filepath = os.path.join(Sl4pConfig.mconfig_dir, 'apps_cfg.json')

                config = self.load_json_as_dict(Sl4pConfig.apps_default_cfg_filepath)
                all_apps_cfg = self.load_json_as_dict(Sl4pConfig.apps_cfg_filepath)

                if _V_apps_config_version != all_apps_cfg.get(_config_version_key, ''):
                    cdprint(1, ("\nWARNING :: Input app-config version ({}) is different from " +
                               "the sl4p library's standard app-config version ({}).").format(
                        all_apps_cfg.get(_config_version_key, ''), _V_apps_config_version
                    ) + "\n        :: " +
                    "Please migrate your app-config. Otherwise some functions may not work or may malfunction.\n")

                app_cfg = all_apps_cfg.get('APPS').get(cfg_param, {})
                cdprint(debugprt, "overriding app cfg : " + str(app_cfg))
                if len(app_cfg):
                    config = override_dict(config, app_cfg)
                else:
                    cdprint(debugprt, "app config '{}' does not exist! sl4p will logging with default config.".format(cfg_param))
            
        else:  # Not-declared CONFIG
            cdprint(debugprt, "Initialize sl4p Logging with default config. (No cfg_param passed)")
            cdprint(debugprt, "Exist default_cfg_file={} : {}".format(Sl4pConfig.file_default_cfg_filepath,
                                                                 os.path.exists(Sl4pConfig.file_default_cfg_filepath)))
            config = self.load_json_as_dict(Sl4pConfig.file_default_cfg_filepath)

        self.defaultConfig = AttributeDict(config.get('LOG', config.get('DEFAULT', config)))
        if not self.defaultConfig.logfile_name:
            self.defaultConfig['logfile_name'] = os.path.splitext(os.path.basename(sys.argv[0]))[0]

        self.customConfig = AttributeDict(config.get('SNIPPET_LOG', config.get('CUSTOM_LOG', {})))
        self.msgFormats = AttributeDict(config.get('MSG_FORMAT'))
        
        self.to_purge_dirs = [self.defaultConfig.logfile_savedir]
        if self.customConfig.use_custom_savedir:
            self.to_purge_dirs.append(self.customConfig.use_custom_savedir)
            
        cdprint(debugprt, "'sl4p' Logging initialized successfully.")

    @classmethod
    def __getInstance(cls, *dummy_args):
        cdprint(cls.debugprt,
                "WARNING :: Sl4p logger already initialized, but cfg_param={} are passed. It will be ignored.".format(
                    str(dummy_args)))
        return cls.__instance
    
    @classmethod
    def instance(cls, cfg_param=''):
        if sys.version_info[0] < 3:
            reload(sys)
            sys.setdefaultencoding(_default_encoding)
        cls.__instance = cls()
        cls.__instance.load(cfg_param, debugprt=Sl4pConfig.debugprt)
        cdprint(cls.debugprt, '-'*40, "\nConfigured Logging Options :")
        cdprint(cls.debugprt, cls.__instance.defaultConfig)
        # cdprint(cls.debugprt, cls.__instance.customConfig)
        if cls.__instance.customConfig.enabled_snippet_dict:
            cdprint(cls.debugprt, "-- Snippets: " + str(cls.__instance.customConfig))
        cdprint(cls.debugprt, '-'*40)
        cls.instance = cls.__getInstance
        EmbeddingHandler.register_embedding(cls.__instance)
        return cls.__instance

    def createInstance(self, cfg_param='', logger_name='', debugprt=0):
        """
        * Unlike singleton Sl4pConfig,  Created sl4pConfig instance DOES NOT SUPPORT embedding-logging and stats
        """
        if sys.version_info[0] < 3:
            reload(sys)
            sys.setdefaultencoding(_default_encoding)
        newInstance = Sl4pConfig()
        newInstance.load(cfg_param, debugprt=debugprt)

        newInstance.debugprt = debugprt

        cdprint(newInstance.debugprt, '-'*40, "\nConfigured Independent Logger <{}> :".format(logger_name))
        cdprint(newInstance.debugprt, newInstance.defaultConfig)
        # cdprint(cls.debugprt, cls.__instance.customConfig)
        cdprint(newInstance.debugprt, '-'*40)
        return newInstance
