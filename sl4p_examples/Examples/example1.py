# -*- coding: utf-8 -*-

import os
import random
import time

from example1sub import ExampleClass
from sl4p import *
from sl4p.src.config import Sl4pConfig

if __name__ == '__main__':
    log = sl4p.getLogger(__file__, './example1_config.json')
    cfg = Sl4pConfig.instance()
    print(os.path.abspath(cfg.defaultConfig.logfile_savedir))

    for i in range(3):
        log.critical('critical message : %d' % i)
        log.error('error message : %d' % i)

        time.sleep(random.random())
        log.warning('warning message : %d' % i)
        time.sleep(random.random())

        log.info('info message : %d' % i)
        log.debug('debug message : %d' % i)

        log.critical('\n')

        example_instance = ExampleClass()
        example_instance.connect()
        example_instance.connect()

        log.warning(u'한글 메시지 출력')
