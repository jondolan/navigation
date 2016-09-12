import time
import struct

_startTime = time.time();
_mouse = open( "/dev/input/mice", "rb" );

def getMouseMovement(mouse):
        _fIn = mouse.read(3);
        return struct.unpack("bb", _fIn[1:]);

while ( 1 ):
	_x, _y = getMouseMovement(_mouse);
	print str(time.time() - _startTime);
	_startTime = time.time();
