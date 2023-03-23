# -*- coding: utf-8 -*-

import time

from sl4p import *

if __name__ == '__main__':

    # Config with dictionary
    # When '{}' is written in logfile_name, It will be a timestamp of %Y%m%d_%H%M%S
    sl4p_cfg_d = dict(LOG={
        'console_level': 'WARNING',

        'logfile_savedir': 'logs',
        'logfile_name': 'EXAMPLE_2_{}'
    })

    with sl4p(__file__, sl4p_cfg_d, debugprt=True) as log:
        for i in range(2):
            log.critical('Critical error occurred!\n')

    with sl4p(__file__) as log:
        log.debug('Loading config of sl4p is singleton design!')
        time.sleep(3)
        log.info('Nice job!')

    with sl4p(__file__, tag='YourTag') as log:
        log.warning('Logging with tag!')

    print('hello')
