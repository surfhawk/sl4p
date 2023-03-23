# -*- coding: utf-8 -*-
import time

from sl4p import *

cfg = dict(LOG={
    'logfile_savedir': 'logs',
    'logging_level': 'DEBUG'
})


def do_iter():
    fac = 1
    for n in range(1, int(200_000)):
        fac = fac * n
    return fac


def hooked_func():
    log.exception('!!!!!!!!!!!!!!!!!!!  Exception occurred !!  Program will exited ...  !!!!!!!!!!!!!!!!!!!')


if __name__ == '__main__':
    # Register hook function when exception occurred
    register_post_exception_terminationf(hooked_func)

    # Profiling CPU and MEMORY usages into csv
    log = sl4p.getLogger(__file__, cfg, stats=(1, './logs/resource_usages.csv'))

    stopwatch = log.create_simpleTimer(log_level='DEBUG')
    stopwatch.start()
    log.info('Timer created and started')
    time.sleep(1)
    stopwatch.check()
    log.info('Timer checked 1')
    time.sleep(1.5)
    stopwatch.check(tag='checked 2:  do_iter start')
    do_iter()
    stopwatch.check(tag='checked 3:  do_iter end')
    log.info('Timer checked 3')

    a = 'a' + 3

    log.info('Program finished.')
