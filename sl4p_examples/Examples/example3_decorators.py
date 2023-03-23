# -*- coding: utf-8 -*-
import time

from sl4p import *

log = sl4p.getLogger(__file__, './example3_config.json')


@sl4p_time()
def my_function1(hello):
    log.info('did you complete your method? {}'.format(hello))
    time.sleep(1.5)
    log.error('not yet...')


@sl4p_time(tag='---> TAG IS HERE <---')
def tagged_function():
    log.info('tagged_function started!')
    time.sleep(2)
    log.info('tagged_function finished!')


@sl4p_try
def take_exception():
    a = 'ABCD' + None


if __name__ == '__main__':
    my_function1('myname')
    take_exception()
    tagged_function()

    log.info('__main__ finished!')
