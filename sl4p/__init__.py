# -*- coding: utf-8 -*-
from .src.api import sl4p, sl4p_try, sl4p_try_exit, sl4p_time, register_post_exception_terminationf
from .src.api import stat_start, stat_stop, example_config_dict

__all__ = ['sl4p', 'sl4p_try', 'sl4p_time', 'sl4p_try_exit', 'register_post_exception_terminationf',
           'stat_start', 'stat_stop', 'example_config_dict']


__version__ = '1.4.2'
__author__ = 'surfhawk@github.com'

__doc__ = " Package 'sl4p' for make logging your python application easy." + \
          " In config.json file, you can find lot's of useful options for production."

__version_changes__ = '\n @ Release Note @' \
                      '\n 1.0.0 :: First deployed release version' \
                      '\n 1.3.1 :: Add log_level for @sl4p_time decorator' \
                      '\n 1.3.2 :: Add log_level for SimpleTimer: logger.create_simpleTimer(), config bugfix' \
                      '\n 1.3.3 :: override_dict bugfix (support python 3.9+)' \
                      '\n 1.4.0 :: Layered apps-config, Support console level&format, IndLogger, Enhance stability' \
                      '\n 1.4.1 :: Correct the docs, Change default config (console config has no initial values)' \
                      '\n 1.4.2 :: Coloring console log (by colorlog) and add related configs, Support console stdout' \
                      '\n @@- Note End -@@'
