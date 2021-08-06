#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int16
from docking import isDocked

from pyzbar import pyzbar
import imutils
import cv2
import enum


class Cmd(enum.Enum):
    N = 2
    S = 8
    E = 6
    W = 4
    X = 5
    CW = 10
    CCW = 11


arduPub = rospy.Publisher('/blinkm', Int16, queue_size=10)

def move(cmd):
    global arduPub
    arduPub.publish(cmd.value)

"""
dispatch
Publishes commands to back up the robot and rotate it for reorientation
Called from true_master.py
Recieves boolean value isDocked from a function called from docking.py
"""
def dispatch():
    if(isDocked()):
        move(Cmd.S)
        rospy.sleep(2)
        move(Cmd.CCW)
        rospy.sleep(11)
        move(Cmd.X)
    else:
        print("Robot must be docked before dispatch")
    return
    
if __name__ == "__main__":
    try:
        dispatch(false)
    except:
        pass