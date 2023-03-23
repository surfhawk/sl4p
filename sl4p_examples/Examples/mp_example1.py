# -*- coding: utf-8 -*-

import time
from multiprocessing import Process

from sl4p import *

cfg = {
    "LOG": {
        "logging_format": "detail",
        "logging_level": "DEBUG",
        "logfile_name": "MP_EXAMPLE_1",
        'logfile_savedir': 'mp_logs',
    }
}

log = sl4p.getLogger(__file__, cfg, debugprt=1)


def do_mprocess(pi):
    llog = sl4p.getLogger(__file__, debugprt=1)
    print("Sub-process {}, logger = {}".format(pi, llog))
    print("Equal?? : {}".format(log == llog))
    for a in ['a', 'b', 'c', 'd', 'e']:
        time.sleep(0.7)
        llog.info("MP {} msg {}!".format(pi, a))


if __name__ == '__main__':

    print("Primary logger = {}".format(log))
    procs = list()

    n_proc = 20
    for i in range(n_proc):
        procs.append(Process(target=do_mprocess, args={"mp_{}".format(i)}))

    for i in range(n_proc):
        procs[i].start()

    for i in range(n_proc):
        procs[i].join()

    log.info("finished!")
