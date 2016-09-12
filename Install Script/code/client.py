import socket
import sys
import struct
import numpy
from math import *
import thread
import time

#HOST = '143.215.94.205'
HOST = '192.168.7.1'
PORT = 8888
TESTING = True # True enables data send to server GUI on specified host:port
if (TESTING):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    print 'Socket Created on PORT ' + str(PORT)

# global variables
_mouseL = open( "/dev/input/mouse1", "rb" );    #open mouse on top right
_mouseR = open( "/dev/input/mouse0", "rb" );    #open mouse on top left

fix = 0.560709878 # constant value to fix data, determined experimentally by pushing robot against wall, rotating 90 degrees, pushing against wall again, and dividing measured angle by 90
rr = 2.125  # raw radius - distance from center of robot to optical sensor (symmetric)
r = rr * fix # fixed radius
scale = 1.0/1515.0 # dpi

dxl = 0.0 # delta of left mouse for each iteration
dyl = 0.0
lupdate = False # does the left mouse have an update?

dxr = 0.0 # delta of right mouse for each iteration
dyr = 0.0
rupdate = False # does the right mouse have an update?
# dleft = (0.0, 0.0) # displacement of left mouse
# dright = (0.0, 0.0) # displacement of right mouse

xw = 0 # x world (center)
yw = 0 # y world (center)
heading = 0 # heading of the robot (axis that runs through the 2 sensors in releation to x axis, perpendicular to direction robot is facing)

def resetValues():
    global xw, yw, heading, dxl, dyl, dxr, dyr, lupdate, rupdate, r, rr, fix
    xw = yw = heading = dxl = dyl = dxr = dyr = 0
    lupdate = rupdate = False
    r = rr * fix

def getMouseMovement(mouse): # read mouse data from /dev/input/mouseX and unpack it into an (dx,dy) coordinate pair
    _fIn = mouse.read(3)
    return struct.unpack("bb", _fIn[1:])

def sendData():
    global xw, yw, heading, s, HOST, PORT
    # s.sendto(str((_deltaX, _deltaY, _deltaX)), (HOST, PORT))
    print '({:.3}, {:.3}): {:.10} degrees.'.format(xw, yw, degrees(heading))

def updatePosition():
    global dxl, dyl, dxr, dyr, lupdate, rupdate, xw, yw, heading
    lupdate = False # we are updating
    rupdate = False
    x = (dxl + dxr)*(scale/2)
    y = (dyl + dyr)*(scale/2)
    t = (dyr - dyl)*(scale/(2*r))
    xw += (x*cos(heading) - y*sin(heading))
    yw += (x*sin(heading) + y*cos(heading))
    heading += t
    if (TESTING): # if we're in testing mode, enables GUI
        sendData()

def updateMouseL():
    global _mouseL, dxl, dyl, lupdate
    while 1: # check if its pushed a new update for both mice (or timeout?)
        dxl, dyl = getMouseMovement(_mouseL)
        lupdate = True
            

def updateMouseR():
    global _mouseR, dxr, dyr, rupdate
    # i = 0
    while 1: # check if its pushed a new update for both mice (or timeout?)
        dxr, dyr = getMouseMovement(_mouseR)
        rupdate = True

thread.start_new_thread(updateMouseR, ())
thread.start_new_thread(updateMouseL, ())
# calibration, triggered by passing "cal" to the script
if len(sys.argv) > 1:
    i = 0
    fix = 1
    TESTING = False
    print "Place the robot against a wall..."
    while i < 3:
        raw_input("Press enter when you're ready to rotate the robot 90 degrees...")
        resetValues()
        print "Rotate...you have 10 seconds..."
        start = time.time()
        while (time.time() - start) < 10:
            if (lupdate & rupdate): # if left and right updated (or timeout?)
                updatePosition()
        if (i == 0):
            fix = abs(heading) / (pi/2)
        else:
            fix = fix / (abs(heading) / (pi/2))
        print "Measured: ", degrees(heading), "This time: ", abs(heading) / (pi/2), "Calibration constant: ", fix
        i+=1
while 1:
    if (lupdate & rupdate): # if left and right updated (or timeout?)
        updatePosition()