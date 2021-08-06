#! /usr/bin/env python


import rospy
import sys
from std_msgs.msg import Int16


def manual():
    publisher = rospy.Publisher('blinkm', Int16, queue_size=1)

    rate =rospy.Rate(0.5)

    hold=5
    counter =0
    print("Enter 0 to stop robot and exit program")
    while(hold != 99):
        if counter >= 100:
            print("Enter direction: ")
	    #Group 18: Added exception handling to the input. If an invalid command is input, the robot is stopped and a new command is prompted for
            try:
                hold=input()
            except:
                print("Invalid command, stopping robot")
		hold = 5
		publisher.publish(hold)
                publisher.publish(5)
            if hold == 0:
                print("Stopping robot and exiting")
                publisher.publish(5)
                return
            counter == 0
        #publisher.publish(hold)
	#Group 18: This condition is left over from one of the previous team. We're unclear on its use.
"""
        if hold == 95:
            publisher.publish(96)
            rospy.sleep(1)
            publisher.publish(31)
            rospy.sleep(12)
            publisher.publish(97)
            rospy.sleep(1)
            publisher.publish(33)
            rospy.sleep(12)
            publisher.publish(96)
            rospy.sleep(1)
            hold = 35
"""
        try:
            publisher.publish(hold)
        except:
            print("Invalid command, stopping robot")
            publisher.publish(5)
        counter +=1

    exit_val=0
    while exit_val != 100:
        publisher.publish(5)
        exit_val += 1
