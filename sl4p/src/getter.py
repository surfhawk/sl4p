# -*- coding: utf-8 -*-
import os
import sys
import re
import platform
import logging
import logging.handlers
from datetime import datetime as dt
from functools import partial
from .utils import make_foldertree_if_not_exists, cdprint
from .const import _logfile_startTs_tpl, _byte_multiples, _default_encoding, _logfile_ext, _root_logger_name
from .stats_performance import SimpleTimer


def get_now_dtStr():
    return dt.now().strftime(_logfile_startTs_tpl)


def disable_inheritance_on_logfile(handler_stream):
    '''
    Preventive code for multiprocessed environment on Windows
    https://stackoverflow.com/questions/948119/preventing-file-handle-inheritance-in-multiprocessing-lib
    https://5kyc1ad.tistory.com/301
    '''
    if str(platform.system()).lower() == 'windows'.lower():  # TODO: hard-coded platform.system
        import msvcrt
        import win32api
        import win32con
        fd = handler_stream.fileno()  # The log handler file descriptor
        fh = msvcrt.get_osfhandle(fd)  # The actual windows handler
        win32api.SetHandleInformation(fh, win32con.HANDLE_FLAG_INHERIT, 0)  #Disable inheritance


def assign_simpleTimer_stubs(logger):
    setattr(logger, 'simpleTimer', SimpleTimer(logger))
    setattr(logger, 'tstart', logger.simpleTimer.start)
    setattr(logger, 'tcheck', logger.simpleTimer.check)

    def create_simpleTimer_with_logger(logger, log_level='debug'):
        return SimpleTimer(logger, log_level)

    create_simpleTimer = partial(create_simpleTimer_with_logger, logger)
    setattr(logger, 'create_simpleTimer', create_simpleTimer)


def get_messageFormatter(fmt, ts_tpl):
    if ts_tpl:
        return logging.Formatter(fmt, ts_tpl)
    else:
        return logging.Formatter(fmt)


def get_filehandler_by_config(config, filepath):
    save_period_type_upper = config.defaultConfig.save_period_type.upper()
    save_period_interval = config.defaultConfig.save_period_interval

    filehandler = None
    if save_period_type_upper.endswith('B'):
        if save_period_type_upper in _byte_multiples:
            filehandler = get_sizedRotatingFileHandler(config, filepath, _byte_multiples.index(save_period_type_upper))
        else:
            cdprint(config.debugprt, "Can not parse {:,} {}' for logfile size-rotating. Use '{:,} MB' instead".format(
                                                save_period_interval, save_period_type_upper, save_period_interval))
            filehandler = get_sizedRotatingFileHandler(config, filepath, 2)
    else:
        filehandler = get_timedRotatingFileHandler(config, filepath)

    return filehandler


def get_sizedRotatingFileHandler(config, filepath, bytemultiple):
    sizedRotatingFileHandler = logging.handlers.RotatingFileHandler(
        filepath,
        maxBytes=config.defaultConfig.save_period_interval * int(1024 ** bytemultiple),
        backupCount=config.defaultConfig.save_files_nlimit,
        encoding=_default_encoding
    )
    return sizedRotatingFileHandler


def get_timedRotatingFileHandler(config, filepath):
    timedRotatingFileHandler = logging.handlers.TimedRotatingFileHandler(
        filepath,
        when= config.defaultConfig.save_period_type,
        interval= config.defaultConfig.save_period_interval,
        backupCount= config.defaultConfig.save_files_nlimit,
        encoding= _default_encoding
    )

    timedRotatingFileHandler.suffix = "{}.{}".format(timedRotatingFileHandler.suffix, _logfile_ext)
    _re_pattern = timedRotatingFileHandler.extMatch.pattern
    _re_pattern = _re_pattern.replace('$', '.{}$'.format(_logfile_ext))

    # suffix_regex = r"" + r"{}".format(_logfile_ext)
    timedRotatingFileHandler.extMatch = re.compile(_re_pattern)

    return timedRotatingFileHandler


def get_root_logger(config, logger_name = ''):
    root_logger = logging.getLogger(logger_name if logger_name else _root_logger_name)

    if not len(root_logger.handlers):
        logCfg = config.defaultConfig
        msgFormats = config.msgFormats

        logfile_name = '{}.{}.{}'.format(logCfg.logfile_name.format(get_now_dtStr()), _root_logger_name, _logfile_ext)
        if logfile_name.startswith('.'):
            logfile_name = logfile_name[1:]

        logfile_savedir = logCfg.logfile_savedir
        logfile_savedir = os.path.abspath(logfile_savedir)
        timestamp_tpl = logCfg.logging_timestamp_tpl

        logfile_path = os.path.join(logfile_savedir, logfile_name)

        make_foldertree_if_not_exists(logfile_savedir)

        msgFormatter = get_messageFormatter(msgFormats.get(logCfg.logging_format), timestamp_tpl)

        fileHandler = get_filehandler_by_config(config, logfile_path)
        fileHandler.setFormatter(msgFormatter)
        fileHandler.setLevel(logCfg.logging_level.upper())
        cdprint(config.debugprt, "*Logger <{}> saving dir= {}\n|".format(_root_logger_name, logfile_savedir))

        root_logger.addHandler(fileHandler)
        if logCfg.use_console_print:
            console_stdout, as_stdout = None, logCfg.get('console_stdout', False)
            if as_stdout:
                console_stdout = sys.stdout

            python_version = sys.version_info
            if (python_version.major >= 3) and (python_version.minor >= 6):  # by colorlog supporting
                import colorlog
                consoleHandler = colorlog.StreamHandler(console_stdout)
                consoleMsgFormatter = colorlog.ColoredFormatter(
                    fmt='%(log_color)s' + msgFormats.get(logCfg.get('console_format', logCfg.logging_format)),
                    datefmt=timestamp_tpl if timestamp_tpl else None,
                    **logCfg.get('console_colorlog_kwargs', {})
                )
            else:
                consoleHandler = logging.StreamHandler(console_stdout)
                consoleMsgFormatter = get_messageFormatter(msgFormats.get(
                    logCfg.get('console_format', logCfg.logging_format)), timestamp_tpl)
            consoleHandler.setFormatter(consoleMsgFormatter)
            consoleHandler.setLevel(logCfg.get('console_level', logCfg.logging_level).upper())
            root_logger.addHandler(consoleHandler)

        root_logger.propagate = False
        root_logger.setLevel('DEBUG')

        disable_inheritance_on_logfile(root_logger.handlers[0].stream)
        assign_simpleTimer_stubs(root_logger)

    return root_logger


def get_custom_logger(config, snippet):
    defaultConfig = config.defaultConfig
    customConfig = config.customConfig
    msgFormats = config.msgFormats

    # assigning custom_logger_name as root-logger-name dot pre-fixed, does logging both root and custom.
    custom_logger_name = '{}.{}'.format(_root_logger_name, snippet.replace('/', '-'))
    custom_logger = logging.getLogger(custom_logger_name)

    if not len(custom_logger.handlers):
        logfile_name = '{}.{}.{}'.format(defaultConfig.logfile_name.format(get_now_dtStr()),
                                         '{}.{}'.format(snippet.replace('/', '-'), _root_logger_name), _logfile_ext)
        if logfile_name.startswith('.'):
            logfile_name = logfile_name[1:]

        custom_savedir = customConfig.use_custom_savedir
        logfile_savedir = custom_savedir if custom_savedir else defaultConfig.logfile_savedir
        logfile_savedir = os.path.abspath(logfile_savedir)
        timestamp_tpl = defaultConfig.logging_timestamp_tpl
        logfile_path = os.path.join(logfile_savedir, logfile_name)

        make_foldertree_if_not_exists(logfile_savedir)

        msgFormatter = get_messageFormatter(msgFormats.get(customConfig.enabled_snippet_dict.get(snippet)),
                                            timestamp_tpl)

        fileHandler = get_filehandler_by_config(config, logfile_path)
        fileHandler.setFormatter(msgFormatter)
        cdprint(config.debugprt, "*Logger <{}> saving dir= {}\n|".format(custom_logger_name, logfile_savedir))

        custom_logger.addHandler(fileHandler)
        custom_logger.setLevel(customConfig.logging_level.upper())
        custom_logger.propagate = customConfig.get('use_propagate', True)

        disable_inheritance_on_logfile(custom_logger.handlers[0].stream)
        assign_simpleTimer_stubs(custom_logger)

    return custom_logger
