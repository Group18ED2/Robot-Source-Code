#! /usr/bin/env python

from docking import dock
from retrieve import retrieve
from publisher import manual
from sensor_msgs.msg import LaserScan
import sys
import rospy

from dispatching import dispatch
 

def laserCallback(msg):
    global distance
    pointCloudSize = len(msg.ranges)
    # for dist in msg.ranges[pointCloudSize-3:pointCloudSize+3]:
    #     distance += dist
    temp = msg.ranges[pointCloudSize/2]
    if(temp <= 10 and temp >= 0.2):
        distance = temp
 
"""
Group 18
true_master.py
Serves as a menu for the robot's functions.
Previously, each script had to be rosrun'd separately.
This was unnecessary and cumbersome, so we added this simple menu to
reference each function easily.
"""
def init():
    rospy.init_node('true_master')
    laserSub = rospy.Subscriber('/scan', LaserScan, laserCallback)
    print("Welcome to the Material Handling Robot.")
    while True:
        print("Please enter the number for a function:")
        print("1:   Manual Control")
        print("2:   Dock")
        print("3:   Dispatch")
        #print("4:   Retrieve")			Commented out due to disconnected push actuator. Should work identically to previous team's work.
        print("0:   Exit")
	try:
        	command = input()
	except:
		print("Invalid command")
		continue
        
        #Tried to map the functions to inputs via a dictionary, but it wasn't working.
        #There are few enough commands to use if/elif without it getting too messy
        if (command == 0):
            sys.exit()
        elif (command == 1):
            manual()
        elif (command == 2):
            dock()
        elif (command == 3):
            dispatch()
        #elif (command == 4):
            #retrieve()
        else:
            print("Invalid Command")

if __name__ == '__main__':
    try:
        init()
    except rospy.ROSInterruptException:
        pass