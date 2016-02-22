import socket
import sys
import struct

#HOST = '143.215.94.205'
HOST = '192.168.7.1'
PORT = 8888

_mouse = open( "/dev/input/mice", "rb" );
_deltaX = 0
_deltaY = 0
#_increment = 0

def getMouseMovement(mouse):
    _fIn = mouse.read(3);
    return struct.unpack("bb", _fIn[1:]);

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit(); # todo - not exit, retry?

print 'Socket Created on PORT ' + str(PORT)

try:
    while ( 1 ): 
        s.sendto(str(getMouseMovement(_mouse)), (HOST, PORT))

        # for more verbose testing
        #_x, _y = getMouseMovement(_mouse)
        #_deltaX += _x
        #_deltaY += _y
        #s.sendto(str((_x, _y)), (HOST, PORT))
        #_increment+=1
        #print str(_increment), ": ", str((_deltaX, _deltaY))


except socket.gaierror:
    print 'Hostname could not be resolved'
    sys.exit()