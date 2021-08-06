#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int16

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

distance = 0.0
prevDiff = 1000.0
prevCmd = Cmd.N
arduPub = rospy.Publisher('/blinkm', Int16, queue_size=10)
distTh = 1.025                                                                  #Group 18: Changed distance threshold from 1.02 to 1.025
def move(cmd):
    print(cmd)
    global arduPub, prevCmd
    prevCmd = cmd
    arduPub.publish(cmd.value)

def controller(diff):
    global distance, prevCmd, prevDiff, distTh
    if(distance > distTh+.25 and diff != 640):                   #Group 18: Changed the condtion for checking the distance to the target. Now there if the robot is between the threshold and threshold+0.25, it will shift left and right to align (see below)
        if(abs(diff) < 85):
            move(Cmd.N)
        elif(diff < -85):
            #if(prevCmd == Cmd.E and abs(prevDiff) < abs(diff)):
            move(Cmd.CW)
            rospy.sleep(0.20)
            move(Cmd.X)
            #else:
            #   move(Cmd.E)
        elif(diff > 85):
            #if(prevCmd == Cmd.W and abs(prevDiff) < abs(diff)):
            move(Cmd.CCW)
            rospy.sleep(0.20)
            move(Cmd.X)
            #else:
            #    move(Cmd.W)
        #elif(abs(diff) > 500):
        #    move(Cmd.X)
    elif(distance <= distTh):
	print(distance)
        move(Cmd.X)
	return False
    elif(diff == 640):
        move(Cmd.CW)
        rospy.sleep(0.2)
        move(Cmd.X)
        rospy.sleep(1)
    elif(distance > distTh and distance <= distTh+.25):                     #Group 18: If the robot is within the 0.25 threshold, it will shift left or right (West or East) to further align the camera with the QR code
	if (diff > 15):
		move(Cmd.W)
		rospy.sleep(0.2)
		move(Cmd.X)
	elif (diff < -15):
		move(Cmd.E)
		rospy.sleep(0.2)
		move(Cmd.X)
	else:
		move(Cmd.N)
    prevDiff = diff
    return True

def scanner(frame, width, height):
    # find the barcodes in the frame and decode each of the barcodes
    barcodeCenter = 0
    barcodes = pyzbar.decode(frame)
    # loop over the detected barcodes
    for barcode in barcodes:
        # extract the bounding box location of the barcode and draw
        # the bounding box surrounding the barcode on the image
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # draw point
        cv2.circle(frame, (int(x + w/2),int(y + h/2)), radius=10, color=(0, 0, 255), thickness=-1)
        cv2.circle(frame, (int(width/2 - 240),int(height/2)), radius=10, color=(0, 255, 0), thickness=-1)          #Group 18: Subtracted 240 from the camera center, since the camera lens isn't fully centered on the robot.
        barcodeCenter = int(x + w/2)
        # the barcode data is a bytes object so if we want to draw it
        # on our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        # draw the barcode data and barcode type on the image
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(frame, text, (x, y - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        # cv2.imshow("image", imutils.resize(frame, width=400))
        # cv2.waitKey(1)
    return (frame, barcodeCenter)

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
isDocked
Checks if the robot is currently docked.
If there is a QR code within 100 pixels of the camera's adjusted center point,
and the distance read by the lidar is LTE to the distance threshold, return True
"""
def isDocked():
    global distance
    vs = cv2.VideoCapture(1)
    rospy.sleep(2)
    width = vs.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = vs.get(cv2.CAP_PROP_FRAME_HEIGHT)
    rec, frame = vs.read()
    newF, barcodeCenter = scanner(frame, width, height)
    diff = (width/2 - 240) - barcodeCenter
    print(diff)
    print(distance)
    vs.release()
    cv2.destroyAllWindows()
    if (abs(diff) < 100 and distance <= distTh):
        return True
    else:
        return False
    
    
"""
Group 18
dock, formerly init
Callable function to dock the robot
"""
def dock():
    laserSub = rospy.Subscriber('/scan', LaserScan, laserCallback)
    shouldMove = True

    # initialize the video stream and allow the camera sensor to warm up
    print("[INFO] starting video stream...")
    vs = cv2.VideoCapture(1)
    rospy.sleep(2)
    width = vs.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = vs.get(cv2.CAP_PROP_FRAME_HEIGHT)
    while shouldMove:                                       #Group 18: Changed condition for while loop. Will now exit when the robot has been stopped at the dock
        # grab the frame from the threaded video stream and resize it to
        # have a maximum width of 400 pixels
        rec, frame = vs.read()
        newF, barcodeCenter = scanner(frame, width, height)
        diff = (width/2 - 240) - barcodeCenter                              #Group 18: Created new variable for the pixel difference between the camera "center" and the QR code center. Subtracted 240 from the camera center, since the camera isn't fully centered on the robot.
        print('Pixel diff is {}'.format(diff))
        shouldMove = controller(diff)
        cv2.imshow("image", imutils.resize(newF, width=400))
        cv2.waitKey(1)
        # cmd = input("Enter Direction: \n")
        # arduPub.publish(int(cmd))
        # rospy.sleep(2)
	    # arduPub.publish(5)
    #vs.release()
    cv2.destroyAllWindows()
    return

if __name__ == '__main__':
    try:
        dock()
    except rospy.ROSInterruptException:
        pass
