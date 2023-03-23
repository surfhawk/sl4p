# -*- coding: utf-8 -*-
from sl4p import *


class ExampleClass(object):
    def __init__(self):
        self.log = sl4p.getLogger(__file__)

    def connect(self):
        self.log.info('db connect log INFO')
        self.log.debug('db connect log DEBUG')
