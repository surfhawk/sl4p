# -*- coding: utf-8 -*-
import json
import os
import sys
from imp import reload
from .utils import cdprint, override_dict
from .const import _apps_default_config_filepath, _apps_config_filepath, _default_encoding
from .embedding import EmbeddingHandler

class AttributeDict(dict): 
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    

class Sl4pConfig(object):
    __instance = None
    debugprt = 0
    stats_enabled = 0
    stats_file = ''
    
    config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'mconfigs')
    
    file_default_cfg_filepath = os.path.join(config_dir, 'cfgf_default.json')
    
    apps_default_cfg_filepath = _apps_default_config_filepath
    apps_cfg_filepath = _apps_config_filepath
    
    #print(default_cfg_file_path, os.path.exists(default_cfg_filepath))
    #print(apps_cfg_filepath, os.path.exists(apps_cfg_filepath))
    
    def load_json_as_dict(cls, cfg_filepath):
        config_str = open(cfg_filepath).read()
        config = json.loads(config_str)
        return config
    
    def load(self, cfg_param=''):
        
        prt = Sl4pConfig.debugprt
        config = None
        
        if cfg_param:
            if isinstance(cfg_param, dict):  # DICT CONFIG
                cdprint(prt, "Initialize sl4p Logging with dictionary= {}".format(cfg_param))
                file_default_config = self.load_json_as_dict(Sl4pConfig.file_default_cfg_filepath)
                config = override_dict(file_default_config, cfg_param)

            elif os.path.exists(cfg_param):  # FILE CONFIG
                cdprint(prt, "Initialize sl4p Logging with configfile= {}".format(cfg_param))
                file_default_config = self.load_json_as_dict(Sl4pConfig.file_default_cfg_filepath)
                file_config = self.load_json_as_dict(cfg_param)
                config = override_dict(file_default_config, file_config)

            else:   # APP CONFIG
                cdprint(prt, "Initialize sl4p Logging with app config '{}'".format(cfg_param))
                cdprint(prt, "Exist apps_default_cfg_file={} : {}".format(Sl4pConfig.apps_default_cfg_filepath,
                                                                          os.path.exists(Sl4pConfig.apps_default_cfg_filepath)))
                cdprint(prt, "Exist apps_cfg_file={} : {}".format(Sl4pConfig.apps_cfg_filepath,
                                                                  os.path.exists(Sl4pConfig.apps_cfg_filepath)))

                config = self.load_json_as_dict(Sl4pConfig.apps_default_cfg_filepath)
                all_apps_cfg = self.load_json_as_dict(Sl4pConfig.apps_cfg_filepath)
                
                app_cfg = all_apps_cfg.get('APPS').get(cfg_param, {})
                cdprint(prt, "overriding app cfg : " + str(app_cfg))
                if len(app_cfg):
                    config = override_dict(config, app_cfg)
                else:
                    cdprint(prt, "app config '{}' does not exist! sl4p will logging with default config.".format(cfg_param))
            
        else:  # Not-declared CONFIG
            cdprint(prt, "Initialize sl4p Logging with default config. (No cfg_param passed)")
            cdprint(prt, "Exist default_cfg_file={} : {}".format(Sl4pConfig.file_default_cfg_filepath,
                                                                 os.path.exists(Sl4pConfig.file_default_cfg_filepath)))
            config = self.load_json_as_dict(Sl4pConfig.file_default_cfg_filepath)
                
        self.defaultConfig = AttributeDict(config.get('DEFAULT'))
        self.customConfig = AttributeDict(config.get('CUSTOM_LOG'))
        self.msgFormats = AttributeDict(config.get('MSG_FORMAT'))
        
        self.to_purge_dirs = [self.defaultConfig.logfile_savedir]
        if self.customConfig.use_custom_savedir:
            self.to_purge_dirs.append(self.customConfig.use_custom_savedir)
            
        cdprint(prt, "'sl4p' Logging initialized successfully.")
    
    
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
        cls.__instance.load(cfg_param)
        cdprint(cls.debugprt, '-'*40, "\nConfigured Logging Options :")
        cdprint(cls.debugprt, cls.__instance.defaultConfig)
        # cdprint(cls.debugprt, cls.__instance.customConfig)
        cdprint(cls.debugprt, '-'*40)
        cls.instance = cls.__getInstance
        EmbeddingHandler.register_embedding(cls.__instance)
        return cls.__instance