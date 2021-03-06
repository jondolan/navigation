import socket
import sys
import struct
import numpy
from math import *
import thread

#HOST = '143.215.94.205'
HOST = '192.168.7.1'
PORT = 8888

# global variables
_mouseL = open( "/dev/input/mouse2", "rb" );    #open mouse on top right
_mouseR = open( "/dev/input/mouse3", "rb" );    #open mouse on top left

fix = 0.931111111
r = 2.125 * fix # distance from center of robot to optical sensor (symmetric)
dleft = (0.0, 0.0) # total displacement of left mouse
dright = (0.0, 0.0) # total displacement of right mouse
xw = 0
yw = 0
heading = 0 # heading of the robot (axis that runs through the 2 sensors in releation to x axis, perpendicular to direction robot is facing)
rupdate = False
lupdate = False
increment = 0
scale = 1.0/1515.0 # dpi
#lock = thread.allocate_lock()

def getMouseMovement(mouse):
    _fIn = mouse.read(3)
    return struct.unpack("bb", _fIn[1:])


def updatePosition():
    global dleft, dright, lupdate, rupdate, xw, yw, heading
    lupdate = False
    rupdate = False
    x = (dleft[0] + dright[0])*(scale/2)
    y = (dleft[1] + dright[1])*(scale/2)
    t = (dright[1] - dleft[1])*(scale/(2*r))
    xw += (x*cos(heading) - y*sin(heading))
    yw += (x*sin(heading) + y*cos(heading))
    heading += t
    print '({:.3}, {:.3}): {:.4} degrees. {:.2}'.format(xw, yw, degrees(heading), float(dleft[0] - dright[0]))

def updateMouseL():
    global _mouseL, dleft, lupdate
    # i = 0
    while 1: # check if its pushed a new update for both mice (or timeout?)
        #i += 1
        d = getMouseMovement(_mouseL)
        dleft = (d[0], d[1])
        #if (i >= 1):
        # dleft = (dleft[0], dleft[1])
        # i = 0
        # dleft = (0, 0)
        lupdate = True
            

def updateMouseR():
    global _mouseR, dright, rupdate
    # i = 0
    while 1: # check if its pushed a new update for both mice (or timeout?)
        #i += 1
        d = getMouseMovement(_mouseR)
        dright = (d[0], d[1])
        #if (i >= 1):
        # dright = (dright[0], dright[1])
        # i = 0
        # dright = (0, 0)
        rupdate = True
            

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit(); # todo - not exit, retry?

print 'Socket Created on PORT ' + str(PORT)

    # while 1: 
    #     thread.start_new_thread(getMouseMovement, (_mouse1, xl, yl, lock))
    #     thread.start_new_thread(getMouseMovement, (_mouse2, xr, yr, lock))

    #     thread.start_new_thread(updatePosition, (lock, ))
    #thread.start_new_thread(updateMouseL, ())

thread.start_new_thread(updateMouseR, ())
thread.start_new_thread(updateMouseL, ())
while 1:
    if (lupdate & rupdate): # if left and right updated (or timeout?)
        updatePosition()
    
    #while 1:
        #updatePosition()
        #updateMouseL()

    

try:
    print 'hey'
except socket.gaierror:
    print 'Hostname could not be resolved'
    sys.exit()



#x0, y0 = getMouseMovement(_mouse0) # todo: threading
    #x1, y1 = getMouseMovement(_mouse1)

    #s.sendto(str(miceCoeff(r0, r1, theta0, phi0, theta1, phi1, x0, y0, x1, y1)), (HOST, PORT))

    #_deltaX, _deltaY, _deltaW = miceCoeff(r0, r1, theta0, phi0, theta1, phi1, x0, y0, x1, y1)
    #print str((_deltaX, _deltaY, _deltaW))
    #s.sendto(str((_deltaX, _deltaY, _deltaX)), (HOST, PORT))
    


    # for more verbose testing
    # _x, _y = getMouseMovement(_mouse)
    # _deltaX += _x
    # _deltaY += _y
    # s.sendto(str((_x, _y)), (HOST, PORT))
    # _increment+=1
    # print str(_increment), ": ", str((_deltaX, _deltaY))