import socket
import sys
import numpy
from math import *
import time

HOST = '127.0.0.1'
PORT = 8888
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
print 'Socket Created on PORT ' + str(PORT)


startArea = ((0,0),(0,30),(20,30),(20,0),(0,0))
tunnel = ((0,30),(0,45),(18,45),(18,30),(0,30))
truck = ((20,0),(20,12),(30,12),(30,0),(20,0))
# boat = ((60,0),(60,24),(96,24),(96,0),(60,0))
# loadingC = ((10,79),(10,84),(25,84),(25,79),(10,79))
# loadingB = ((40,79),(40,84),(55,84),(55,79),(40,79))
# loadingA = ((65,79),(65,84),(80,84),(80,79),(65,79))
# center = ((43.5,46.5),(43.5,49.5),(51.5,49.5),(51.5,46.5),(43.5,46.5))
# box1 = ((85,69),(85,80),(93,80),(93,69),(85,69))
# box2 = ((85,57),(85,68),(93,68),(93,57),(85,57))
# box3 = ((85,45),(85,56),(93,56),(93,45),(85,45))
# box4 = ((85,33),(85,44),(93,44),(93,33),(85,33))
# areaA = ((0,84),(0,94),(32,94),(32,84),(0,84))
# areaB = ((32,84),(32,94),(64,94),(64,84),(32,84))
# areaC = ((64,84),(64,94),(96,94),(96,84),(64,84))
# board = (startArea, tunnel, truck, boat, loadingA, loadingB, loadingC, center, box1, box2, box3, box4, areaA, areaB, areaC)

xw = 0.0
yw = 0.0
heading = 0.0

# overall philosophy
    # separate decision from execustion
    # decision descides what location to move to next, and passes the corresponding x, y, t to move to to execution
    # execution should be given an x, y, t to move to and it should perform it's own path planning
        # rotation does not to occur to move, omniwheels
        # right angles!!!
            # move first in whichever direction requires most change, then the other direction
        # create a path, check it for collisions
        # rotate at end

def sendData():
    global xy, yw, heading
    s.sendto(str((xw, yw, heading)), (HOST, PORT))
    print '({:.3}, {:.3}): {:.10} degrees.'.format(xw, yw, degrees(heading))

def moveRobot(x, y): # move center to absolute position
    if (abs(xw - x) > abs(yw - y)): # if we have to move more x than y, move x first
        path = ((xw, yw), (x, yw), (x, y))
    else:
        path = ((xw, yw), (xw, y), (x, y))
    travelPath(path)

def checkForCollisions(path): # check for collisions along a path
    return True

def travelPath(path): # expects path in the form of origin, point1, point2 and each change only changes by 1 x or y value, recursive
    print path
    if (len(path) < 2): # need a start and an end
        return
    if (checkForCollisions(path[0:1]) == True):
        sendMotorCommand(path[1][0], path[1][1])
    # else: we cannot travel on this path, checkForCollisions should pass back the source of collision to adjust off of
    travelPath(path[1:]) # recurse

def sendMotorCommand(x, y): # expects a global x, y (absolute) (fakes it currently)
    global xw, yw
    x = xw - x
    y = yw - y
    change = -0.1
    if (x < 0.0) | (y < 0.0): # also need to account for change that is less than 0.1, justsubtract that value
        change = -change
    if (round(x, 2) == 0.0):
        while round(y, 2) != 0.0:
            yw += change
            y += change
            sendData()
            time.sleep(0.01)
    else:
        while round(x,2) != 0.0:
            xw += change
            x += change
            sendData()
            time.sleep(0.01)



moveRobot(25.0, 15.0)

# while 1: # nav loop
#     xw += 0.1
#     yw += 0.1
#     heading += 1
#     sendData()
#     time.sleep(0.25)