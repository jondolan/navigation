import socket
import sys
import struct

_mouse = open( "/dev/input/mice", "rb" );
host = '143.215.94.205'
port = 8888
_deltaX = 0
_deltaY = 0
#increment = 0

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

print 'Socket Created on port ' + str(port)

try:
    while ( 1 ):
    	#_x, _y = getMouseMovement(_mouse)
    	#_deltaX += _x
    	#_deltaY += _y
        s.sendto(str(getMouseMovement(_mouse)), (host, port))
    	#s.sendto(str((_x, _y)), (host, port))
    	#increment+=1
    	#print str((_deltaX, _deltaY)) 

except socket.gaierror:
    #could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()
