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

# global variables
_mouseL = open( "/dev/input/mouse2", "rb" );    #open mouse on top right
_mouseR = open( "/dev/input/mouse3", "rb" );    #open mouse on top left
fl = open("left.txt", "w+")
fr = open("right.txt", "w+")

r = 4.5 # distance from center of robot to optical sensor (symmetric)
r = 0.05
left = (0.0, 0.0) # total displacement of left mouse
right = (2*r, 0.0) # total displacement of right mouse
heading = 0 # heading of the robot (axis that runs through the 2 sensors in releation to x axis, perpendicular to direction robot is facing)
rupdate = False
lupdate = False
increment = 0
scale = 500.0 # dpi
#lock = thread.allocate_lock()

def getMouseMovement(mouse):
    _fIn = mouse.read(3)
    return struct.unpack("bb", _fIn[1:])


def updatePosition():
    global left, right, lupdate, rupdate
    lupdate = False
    rupdate = False
    # if (increment % 250) == 0:
    #heading = numpy.arctan2((right[1]+dright[1])-(left[1]+dleft[1]), (right[0]+dright[0])-(left[0]+dleft[0])) + pi/2 # because theta is through the front 2 wheels
    heading = numpy.arctan2((right[1] - left[1]), (right[0] - left[0])) + pi/2
    #print (yr+dyr)-(yl+dyl), (xr+dxr)-(xl+dxl)
    #print degrees(bearing)
    # left = (left[0] + dleft[0]/scale, left[1] + dleft[1]/scale)
    # right = (right[0] + dright[0]/scale, right[1] + dright[1]/scale)    
    #centerX = xl + (r/2)*cos(bearing)
    #centerY = yl + (r/2)*sin(bearing)
    centerX = (left[0] + right[0]) / 2.0
    centerY = (left[1] + right[1]) / 2.0
    fl.write('{:.4} {:.4}\n'.format(left[0], left[1]))
    fr.write('{:.4} {:.4}\n'.format(right[0], right[1]))
    print '({:.3}, {:.3}), ({:.3}, {:.3}): {:.4} degrees'.format(left[0], left[1], right[0], right[1], degrees(heading))

def updateMouseL():
    global _mouseL, left, lupdate
    i = 0
    dl = (0, 0)
    while 1: # check if its pushed a new update for both mice (or timeout?)
        i += 1
        d = getMouseMovement(_mouseL)
        dl = (dl[0] + d[0], dl[1] + d[1])
        #print 'right: ', str(dright)
        if (i >= 25):
            dleft = (dl[0] / i, dl[1] / i)
            #print 'left: ', str(dleft)
            left = (left[0] + dleft[0]/scale, left[1] + dleft[1]/scale)
            i = 0
            dl = (0, 0)
            lupdate = True
            

def updateMouseR():
    global _mouseR, right, rupdate
    i = 0
    dr = (0, 0)
    while 1:
        i += 1
        d = getMouseMovement(_mouseR)
        dr = (dr[0] + d[0], dr[1] + d[1])
        #print 'right: ', str(dright)
        if (i >= 25):
            dright = (dr[0] / i, dr[1] / i)
            #print dright
            right = (right[0] + dright[0]/scale, right[1] + dright[1]/scale)
            i = 0
            dr = (0, 0)
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