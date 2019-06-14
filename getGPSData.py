# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 16:23:08 2019

@author: Oliver
"""

from pymavlink import mavutil
import time

master = mavutil.mavlink_connection(
            '/dev/serial0',
            baud=115200)

master.wait_heartbeat()

# Request all parameters
master.mav.param_request_list_send(
    master.target_system, master.target_component
)

while True:
    time.sleep(0.01)
    try:
        message = master.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
        print('name: %s\tvalue: %d' % (message['param_id'].decode("utf-8"), message['param_value']))
    except Exception as e:
        print(e)
        exit(0)