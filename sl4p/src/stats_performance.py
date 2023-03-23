# -*- coding: utf-8 -*-
import uuid
import time
import os
import psutil
from datetime import datetime as dt
from multiprocessing import Process
from .utils import cdprint


class SimpleTimer(object):
    def __init__(self, logger, log_level='debug'):
        self.logger = logger
        self.log_level = log_level.lower()
        self.logging_func = getattr(logger, self.log_level)
    
    def start(self, tag=''):
        self.tm_uuid = str(uuid.uuid4())[:6]
        self.st_t = time.time()
        self.logging_func("    * Timer  %s---------- /%s  Started" % (
            " ({}) ".format(tag).rjust(60, '-') if tag else '-' * 60, self.tm_uuid))
        
    def check(self, tag=''):
        self.logging_func("    * Timer  %s---------- /%s  Checked at  %10.4f s" % (
            " ({}) ".format(tag).rjust(60, '-') if tag else '-' * 60, self.tm_uuid, time.time() - self.st_t))


class SimpleStatCpuMem(object):
    debugprt = 0
    mproc = None

    stat_fp = None
    _stat_start_dt = None
    _stat_end_dt = None

    @classmethod
    def stat_start(cls, config):
        cls.debugprt = config.debugprt
        # TODO: need psutil missing halt.?
        
        _ts = dt.now().strftime("%Y%m%d_%H%M%S")
        statfile_path = os.path.abspath(config.stats_file) if config.stats_file else ''
        _fp = os.path.abspath(statfile_path) if statfile_path else os.path.abspath("stats_cpumem_{}.csv".format(_ts))
        cls.stat_fp = _fp
        
        cdprint(cls.debugprt, "[ -- Performance Test : CPU and MEMORY usage --> {}  ]".format(cls.stat_fp))
        
        cls.mproc = Process(target=write_cpu_mem_usage, args=(cls.stat_fp,))
        cls._stat_start_dt = dt.now()
        cls.mproc.start()
        time.sleep(2)
    
    @classmethod
    def stat_stop(cls):
        if cls.mproc:
            time.sleep(3)
            cls.mproc.terminate()
            cdprint(cls.debugprt, "[ -- Testing resource usage finished !!! -- ]")
            cls._stat_end_dt = dt.now()
            try:
                stat_elapsed = (cls._stat_end_dt - cls._stat_start_dt).total_seconds()
                with open(cls.stat_fp, 'a+') as f:
                    f.write(",StatCpuMem Elapsed: {:.4f}s,\n".format(stat_elapsed))
            except Exception as e:
                cdprint(cls.debugprt,
                        "Exception occurred on f`stat_stop !!  Writing elapsed time failed - '{}'".format(e))


stat_start = SimpleStatCpuMem.stat_start
stat_stop = SimpleStatCpuMem.stat_stop


def write_cpu_mem_usage(fp):
    with open(fp, 'a+') as f:
        f.write("Timestamp,CPU_percent,MEM_percent,MEM_usage_GB\n")
        cnt = 0
        while True:
            
            _dt_str = dt.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            _cpu_percent = psutil.cpu_percent()
            _memstat = psutil.virtual_memory()
            _mem_percent = _memstat[2]
            _mem_usage = round(_memstat[3] / 1073741824.0, 2)
            f.write("{},{},{},{}\n".format(_dt_str, _cpu_percent, _mem_percent, _mem_usage))
            
            time.sleep(0.33)
            
            cnt += 1
            if cnt > 6:
                cnt = 0
                f.flush()
