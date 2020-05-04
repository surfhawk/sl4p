# -*- coding: utf-8 -*-

from .context import sl4p
from .decorators import sl4p_try
from .decorators import sl4p_time
from .embedding import register_post_exception_terminationf
from .stats_performance import stat_start
from .stats_performance import stat_stop

_sl4p_example_config_dict = {
    "DEFAULT": {
        "logging_level": "DEBUG",
        "logging_format": "detail",
        "logging_timestamp_tpl": "%Y.%m.%d-%H:%M:%S",

        "logfile_savedir": "./sl4p_logs",
        "logfile_name": "LOG.EXAMPLE_APP",

        "save_period_type": "MB",
        "save_period_interval": 300,
        "save_files_nlimit": 5,

        "purge_window_hours": 240,
        "use_console_print": True
    },
}