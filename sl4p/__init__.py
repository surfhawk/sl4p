# -*- coding: utf-8 -*-
from .src.api import sl4p, sl4p_try, sl4p_time, register_post_exception_terminationf, stat_start, stat_stop
from .src.api import _example_config_dict

__all__ = ['sl4p', 'sl4p_try', 'sl4p_time', 'register_post_exception_terminationf', 'stat_start', 'stat_stop',
           '_example_config_dict']


__version__ = '1.2.0'
__author__ = 'surfhawk@github'

__doc__ = " Package 'sl4p' for make logging your python application easy."  + \
          " In config.json file, you can find lot's of useful options for production."

__version_changes__ = '\n @ Release Note @' \
                      '\n 1.0.0 :: First deployed release version' \
                      '\n @@- Note End -@@'