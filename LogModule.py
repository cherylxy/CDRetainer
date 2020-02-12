# -*- coding: gbk -*-
# ==========================================================================
#   Copyright (C) 2015-2020 All rights reserved.
#
#   filename : LogModule.py
#   author   : chendian / okcd00@qq.com
#   date     : 2015-11-10
#   desc     : Logging module for easy changing.
# ==========================================================================

import os
import sys
import time
import logging
from importlib import reload
import configparser as ConfigParser

# CONFIG SET
config = ConfigParser.ConfigParser()
config.read("./conf/basic.conf")
path_log = config.get("path", "path_log")


class LogModule(object):

    Log = path_log
    LastTime = 0
    LastDate = "Last Recorded Date"
    CurrentDate = "Current Date"

    logger = logging.getLogger()
    handler = logging.FileHandler(Log)
    logger.addHandler(handler)
    logger.setLevel(logging.NOTSET)

    reload(sys)
    # sys.setdefaultencoding('utf-8')  # deprecated in py3

    def __init__(self):
        self.LastTime = time.localtime(time.time())
    
    def getTime(self):
        return str(time.strftime('%m-%d %H:%M:%S', time.localtime(time.time())))
    
    def Warning(self, tstring):
        self.logger.info("[Warning] %s " % str(tstring) + self.getTime())
        
    def Fatal(self, tstring):
        self.logger.info("[Fatal] %s " % str(tstring) + self.getTime())
        
    def Notice(self, tstring):
        self.logger.info("[Notice] %s " % str(tstring) + self.getTime())
        
    def CheckLog(self, Log):
        if os.path.exists(Log):
            return True
        else:
            return False