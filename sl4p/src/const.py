# -*- coding: utf-8 -*-
import os
from .utils import get_os_userhome_dirpath

_default_encoding = 'utf-8'
_root_logger_name = 'sl4p'
_logfile_ext = 'log'
_logfile_startTs_tpl = '%Y%m%d_%H%M%S'

_apps_default_cfg_fn = 'apps_default.json'
_apps_cfg_fn = 'apps_cfg.json'

_os_user_homedir = get_os_userhome_dirpath()
_apps_default_config_filepath = os.path.join(_os_user_homedir, 'sl4p_configs', _apps_default_cfg_fn)
_apps_config_filepath = os.path.join(_os_user_homedir, 'sl4p_configs', _apps_cfg_fn)


# META INFORMATION FOR VALIDATION
_config_version_key = '__configver__'
_V_default_config_version = 'C4'
_V_apps_config_version = 'APP_C4'

_byte_multiples = ['B', 'KB', 'MB', 'GB']
