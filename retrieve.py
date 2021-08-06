from retrieval_master import moveToShelf
from retrieval import retrieveBin

"""
Group 18
retrieve
Combines the actions from previous programs retrieval_master.py and retrieval.py, 
which moved the robot to the located shelf, and retrieved the bin from the shelf, respectively
![Untested, the push actuator on the robot's tray was disconnected when we received it,
 and we were unable to find the proper schematics to identify where and how it was
 connected to the system previously. Given a properly connected actuator, this
 functionality should work identically with how the previous team left it, just condensed.]!
"""
def retrieve():
	moveToShelf()
	retrieveBin()