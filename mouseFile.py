# import libraries
import mouse
# library for retreiving mouse data
import struct

# read mouse movement from file
def getMouseMovement(mouse):
	_fIn = mouse.read(3);
	return struct.unpack("bb", _fIn[1:]);


# global variables
_mouse = open( "/dev/input/mice", "rb" ); # open the mouse
_deltaX = 0;
_deltaY = 0;
_dotsPerInch = 2000.0;
fOut = open('movement.txt', 'w');


while (1):
	_x, _y = getMouseMovement(_mouse);
	_deltaX += _x;
	_deltaY += _y;
	print("Dots: (" + str(_deltaX) + "," + str(_deltaY) + ")\nInches: (" + str(_deltaX/_dotsPerInch) + "," + str(_deltaY/_dotsPerInch) + ")\n");
	fOut.write("Dots: (" + str(_deltaX) + "," + str(_deltaY) + ")\nInches: (" + str(_deltaX/_dotsPerInch) + "," + str(_deltaY/_dotsPerInch) + ")\n");
	
fOut.close();