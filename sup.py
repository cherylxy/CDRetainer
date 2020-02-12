# -*- coding: gbk -*-
# ==========================================================================
#   Copyright (C) 2015-2020 All rights reserved.
#
#   filename : sup.py
#   author   : chendian / okcd00@qq.com
#   date     : 2015-11-10
#   desc     : Support or SubProcess Module for Issue `Errno.110`
# ==========================================================================

import time
from LogModule import LogModule
import subprocess as commands
import configparser as ConfigParser


l = LogModule()
config = ConfigParser.ConfigParser()  
config.read("./conf/basic.conf")
exec_cycle_time = config.getint("para", "EXEC_CYCLE_TIME")


if __name__ == '__main__':
    LastTime = -1   
    while True:
        CurrentTime = time.time()
        if CurrentTime - LastTime > exec_cycle_time:
            LastTime = CurrentTime
            # os.system('nohup python CDRetainer.py &')
            l.Notice("Sup_Process Start. Loading CDRetainer...")
            (status, output) = commands.getstatusoutput('nohup python CDRetainer.py \&')
            l.Notice("Retainer Finished. Status: {}\nOutput: {}".format(str(status), str(output)))