import socket
import sys
import numpy
from math import *
import time
import thread
import os
import signal
import struct

import random

PORT = 1337
beagle0 = ('192.168.1.100', PORT) # motors 0 and 3 ( in that order)
beagle1 = ('192.168.1.101', PORT) # motors 1 and 2 (in that order)
HOST = ''
PORT = 8888
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
print 'Socket Created on PORT ' + str(PORT)

ISGAMELEFT = False # if the robot must move LEFT to hit a wall first, game type is left

xw = 0.0 if ISGAMELEFT else 96.0
yw = 0.0
heading = 0.0
robotsize = 11.5

speed = struct.pack("f", 2.0)
motorCoef = (0, 0, 0, 0)
motorCW = (struct.pack("i", motorCoef[0]), struct.pack("i", motorCoef[1]), struct.pack("i", motorCoef[2]), struct.pack("i", motorCoef[3])) # motor 0, 1, 2, 3 requires 0 or 1 to move clockwise
motorCCW = (struct.pack("i", 1-motorCoef[0]), struct.pack("i", 1-motorCoef[1]), struct.pack("i", 1-motorCoef[2]), struct.pack("i", 1-motorCoef[3])) # motor 0, 1, 2, 3 requires 0 or 1 to move clockwise

mm2in = 0.03937008

deadReckon = ((-12, 84, 0)) if ISGAMELEFT else ((108, 84, 0))

startArea = ((0,0),(0,30),(20,30),(20,0),(0,0)) if ISGAMELEFT else ((96,0),(96,30),(76,30),(76,0),(96,0))
tunnel = ((0,30),(0,45),(18,45),(18,30),(0,30)) if ISGAMELEFT else ((96,30),(96,45),(78,45),(78,30),(96,30))
truck = ((20,0),(20,12),(30,12),(30,0),(20,0)) if ISGAMELEFT else ((76,0),(76,12),(66,12),(66,0),(76,0))
boat = ((60,0),(60,24),(96,24)) if ISGAMELEFT else ((36,0),(36,24),(0,24))
box1 = ((85,69),(85,80)) if ISGAMELEFT else ((11,69),(11,80))
box2 = ((85,57),(85,68)) if ISGAMELEFT else ((11,57),(11,68))
box3 = ((85,45),(85,56)) if ISGAMELEFT else ((11,57),(11,68))
box4 = ((85,33),(85,44)) if ISGAMELEFT else ((11,57),(11,68))
boxes = (box1, box2, box3, box4)
rail = (0, 0, 0, 0)
zoneA = ((96,84),(64,84)) if ISGAMELEFT else ((0,84),(32,84))
zoneB = ((64,84),(32,84)) if ISGAMELEFT else ((64,84),(32,84))
zoneC = ((32,84),(0,84)) if ISGAMELEFT else ((96,84),(64,84))
# board = (startArea, tunnel, truck, boat, box1, box2, box3, box4, zoneA, zoneB, zoneC)

# RGBY
ABlocks = (0, 0, 16, 0) # 16 blue blocks, each 5 inches and worth 3 points, no QR code
AILoc = (boat[1][0], zoneA[1][1]-robotsize, 0)
ALoc = (zoneA[1][0], zoneA[1][1]-robotsize/2.0, 0)
AIDests = ((boat[1][0]-robotsize if ISGAMELEFT else boat[1][0]+robotsize, zoneA[1][1]-robotsize, 90 if ISGAMELEFT else 270),
           (boat[1][0]-robotsize if ISGAMELEFT else boat[1][0]+robotsize, zoneA[1][1]-robotsize, 90 if ISGAMELEFT else 270),
           (boat[1][0]-robotsize if ISGAMELEFT else boat[1][0]+robotsize, zoneA[1][1]-robotsize, 90 if ISGAMELEFT else 270),
           (boat[1][0]-robotsize if ISGAMELEFT else boat[1][0]+robotsize, zoneA[1][1]-robotsize, 90 if ISGAMELEFT else 270))
ADests = ((boat[1][0], boat[1][1] / 2.0, 90 if ISGAMELEFT else 270),
          (boat[1][0], boat[1][1] / 2.0, 90 if ISGAMELEFT else 270),
          (boat[1][0], boat[1][1] / 2.0, 90 if ISGAMELEFT else 270),
          (boat[1][0], boat[1][1] / 2.0, 90 if ISGAMELEFT else 270)) # all go to the boat
ARDest = (boat[1][0]-robotsize if ISGAMELEFT else boat[1][0]+robotsize, boat[1][1] / 2.0, 90 if ISGAMELEFT else 270)

BBlocksSmall = (2, 2, 2, 2) # 2 of each color, each 2.5 inches and worth 10 points
BBlocks = (3, 3, 3, 3) # 3 of each color, each 5 inches and worth 15 points
BILoc =  (zoneB[1][0], zoneB[1][1]-robotsize/2.0, 0)
BLoc = ((zoneB[0][0] + zoneB[1][0]) / 2.0, zoneB[0][1], 0)
BDests = () # blocks go to respective containers, determined on fly becuase random

CBlocks = (4, 4, 4, 4) # 4 of each color, each 5 inches, rgy worth 5 points and blue 3
CILoc =  (zoneC[1][0], zoneC[1][1]-robotsize/2.0, 0)
CLoc = ((zoneC[0][0] + zoneC[1][0]) / 2.0, zoneC[0][1], 0)
CDests = ((truck[2][0], truck[2][1], 270 if ISGAMELEFT else 90),
          (truck[2][0], truck[2][1], 270 if ISGAMELEFT else 90),
          ADests[0],
          (truck[2][0], truck[2][1], 270 if ISGAMELEFT else 90)) # blue goes to boat rest go to truck


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
    #print '({:.3}, {:.3}): {:.10} degrees.'.format(xw, yw, degrees(heading))

def moveRobot(c): # move center to absolute position
    if (c == (0,0,0)):
        return
    x = c[0]
    y = c[1]
    t = c[2]
    if (abs(xw - x) > abs(yw - y)): # if we have to move more x than y, move x first
        path = ((xw, yw), (x, yw), (x, y))
    else:
        path = ((xw, yw), (xw, y), (x, y))
    travelPath(path)
    rotateRobot(t)

# move robot in relation to game board
# diagonal motors spin same direction
# beagle0 motors 0 and 3 ( in that order)
# beagle1 motors 1 and 2 (in that order)
def moveRobotUp(): # motor 0/1 cw, motor 3/2 ccw
    s.sendto(speed + motorCW[0] + speed + motorCCW[3], beagle0)
    s.sendto(speed + motorCW[1] + speed + motorCCW[2], beagle1)

def moveRobotDown(): # motor 0/1 ccw, motor 3/2 cw
    s.sendto(speed + motorCCW[0] + speed + motorCW[3], beagle0)
    s.sendto(speed + motorCCW[1] + speed + motorCW[2], beagle1)

def moveRobotLeft(): # motor 0/3 cw, motor 1/2 ccw
    s.sendto(speed + motorCW[0] + speed + motorCW[3], beagle0)
    s.sendto(speed + motorCCW[1] + speed + motorCCW[2], beagle1)

def moveRobotRight(): # motor 0/3 cww, motor 1/2 cw
    s.sendto(speed + motorCCW[0] + speed + motorCCW[3], beagle0)
    s.sendto(speed + motorCW[1] + speed + motorCW[2], beagle1)

def rotateRobot(t): # robot ccw all wheels go cw
    global heading
    heading = t
    sendData()

def travelPath(path): # expects path in the form of origin, point1, point2 and each change only changes by 1 x or y value, recursive
    if (len(path) < 2): # need a least start and an end
        return
    sendMotorCommand(path[1][0], path[1][1])
    # else: we cannot travel on this path, checkForCollisions should pass back the source of collision to adjust off of
    travelPath(path[1:]) # recurse

def sendMotorCommand(x, y): # expects a global x, y (absolute)
    global xw, yw
    dx = x - xw
    dy = y - yw
    print 'Move from (', round(xw, 5), ', ', round(yw, 5), ') to (', x, ', ', y, ')'
    
    if (round(dx, 4) == 0.0): # robot moves up or down
        if (dy > 0):
            direction = 0 # moveRobotUp()
        else:
            direction = 2 # moveRootDown()
    else:
        if (dx > 0):
            direction = 1
        else:
            direction = 3
 
    direction += 4 - int(round(heading / 90))
    direction = direction & 3



    if direction == 0:
        moveRobotUp()
    elif direction == 1:
        moveRobotRight()
    elif direction == 2:
        moveRobotDown()
    else:
        moveRobotLeft()


    change = 0.2
    if (round(dx, 4) == 0.0):
        while abs(round(dy, 4)) > 0.1:
            yw += copysign(change, dy)
            dy -= copysign(change, dy)
            sendData()
            time.sleep(0.01)
    else:
        while abs(round(dx, 4)) > 0.1:
            xw += copysign(change, dx)
            dx -= copysign(change, dx)
            sendData()
            time.sleep(0.01)

def getD1():
    return True

def get2():
    return True

def getD3():
    return True

def grabBlock(): # hone in on the bloc location and then set the yw accordingly
    global yw
    time.sleep(1)
    colors = ['red', 'green', 'blue', 'yellow']
    return colors[random.randrange(0, 4, 1)]

def getQR():
    return 'red'

def determineRailOrder():
    global rail, boxes
    railTmp = []
    moveRobot((boxes[0][0][0], boxes[0][0][1], 90 if ISGAMELEFT else 275)) # box 1
    # railTmp[0] = getQR()
    moveRobot((boxes[1][0][0], boxes[1][0][1], 90 if ISGAMELEFT else 275))
    # railTmp[1] = getQR()
    moveRobot((boxes[2][0][0], boxes[2][0][1], 90 if ISGAMELEFT else 275))
    # railTmp[2] = getQR()
    moveRobot((boxes[3][0][0], boxes[3][0][1], 90 if ISGAMELEFT else 275))
    # railTmp[3] = getQR()
    railTmp = ['red', 'blue', 'yellow', 'green']
    for i in range(0, len(railTmp)):
        if railTmp[i] == 'red':
            rail = (boxes[i], rail[1], rail[2], rail[3])
        elif railTmp[i] == 'green':
            rail = (rail[0], boxes[i], rail[2], rail[3])
        elif railTmp[i] == 'blue':
            rail = (rail[0], rail[1], boxes[i], rail[3])
        elif railTmp[i] == 'yellow':
            rail = (rail[0], rail[1], rail[2], boxes[i])

def createBDests():
    global rail, BDests
    BDests = ((rail[0][0][0], (rail[0][0][1] + rail[0][1][1]) / 2.0, 90 if ISGAMELEFT else 275),
              (rail[1][0][0], (rail[1][0][1] + rail[1][1][1]) / 2.0, 90 if ISGAMELEFT else 275),
              (rail[2][0][0], (rail[2][0][1] + rail[2][1][1]) / 2.0, 90 if ISGAMELEFT else 275),
              (rail[3][0][0], (rail[3][0][1] + rail[3][1][1]) / 2.0, 90 if ISGAMELEFT else 275))

def gameTimerLoop():
    time.sleep(300)
    os.kill(os.getpid(), signal.SIGINT)


def waitForStart():
    raw_input("Press Enter to start program...")
    thread.start_new_thread(gameTimerLoop, ())


waitForStart()

moveRobot(deadReckon) # move robot to corner of zone C, will not actually get the center there
# d1 = getD1() # home location with distance sensors
# while d1 != 50: # tolerance?
#     if (d1 < 50):
#         moveRobotBackward()
#     else:
#         moveRobotForward()
#     d1 = getD1()
# d2 = getD2()
# while d2 != 50: # tolerance?
    # if (d2 < 50):
    #     if (ISGAMELEFT):
    #         moveRobotRight()
    #     else:
    #         moveRobotLeft()
    # else:
    #     if (ISGAMELEFT):
    #         moveRobotLeft()
    #     else:
    #         moveRobotRight()
    # d2 = getD2()
moveRobot((7, 77, 0) if ISGAMELEFT else ((89, 77, 0))) # to be removed, but home it in the simulation
xw = 7 if ISGAMELEFT else 89
yw = 77
heading = 0


dests = 'AA'
i = 0
for i in range(0, len(dests)):
    loc = dests[i]
    dest = ()
    if loc == 'A':
        moveRobot(AILoc)
        moveRobot(ALoc)
        idest = AIDests
        dest = ADests
        rdest = ARDest
    elif loc == 'B':
        moveRobot(BILoc)
        moveRobot(BLoc)
        dest = BDests
    elif loc == 'C':
        moveRobot(CILoc)
        moveRobot(CLoc)
        dest = CDests

    time.sleep(0.5)
    block = grabBlock()
    print "Picked up a ", block, " block"

    if (dest == BDests) & (len(BDests) == 0):
        determineRailOrder()
        createBDests()
        dest = BDests

    if block == 'red':
        moveRobot(idest[0])
        moveRobot(dest[0])
    elif block == 'green':
        moveRobot(idest[1])
        moveRobot(dest[1])
    elif block == 'blue':
        moveRobot(idest[2])
        moveRobot(dest[2])
    elif block == 'yellow':
        moveRobot(idest[3])
        moveRobot(dest[3])

    time.sleep(1)

    moveRobot(rdest)

    i+=1