#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import logging
import time

logging.basicConfig(level=logging.INFO)
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_2_CH_SCR_HAL import SCR

# scr = SCR.SCR(dev = "/dev/ttySC0",data_mode = 1)
scr = SCR.SCR(data_mode=0)  # 0:I2C  1: UART
angle = 0
try:
    scr.SetMode(1)
    scr.VoltageRegulation(1, 0)
    scr.VoltageRegulation(2, 0)
    scr.ChannelEnable(1)
    scr.ChannelEnable(2)
    # while(1):
    # time.sleep(0.2)
    while (1):
        time.sleep(0.2)
        if (angle < 180):
            scr.VoltageRegulation(1, angle % 180)
            scr.VoltageRegulation(2, angle % 180)
        else:
            scr.VoltageRegulation(1, 180 - angle % 180)
            scr.VoltageRegulation(2, 180 - angle % 180)
        angle = angle + 1
        if (angle > 360):
            angle = 0

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    scr.ChannelDisable(1)
    scr.ChannelDisable(2)
    scr.VoltageRegulation(1, 0)
    scr.VoltageRegulation(2, 0)
    exit()
