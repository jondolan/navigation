import struct
import time
import sys
import libraries.console
import curses

_mouse0 = open( "/dev/input/mouse0", "rb" );
_mouse1 = open( "/dev/input/mouse1", "rb" );

_startTime = time.time(); # start of script execution
_deltaX = 0;
_deltaY = 0;
_maxX = 0;
_maxY = 0;
_winScaleX = 50; #console.getTerminalSize()[0] / 10;
_winScaleY = 50; #console.getTerminalSize()[1] / 10;
_countX = libraries.console.getTerminalSize()[0] / 2;
_countY = libraries.console.getTerminalSize()[1] / 2;

window = curses.initscr();

def getMouseMovement(mouse):
	_fIn = mouse.read(3);
	return struct.unpack("bb", _fIn[1:]);

while( 1 ):
	_x, _y = getMouseMovement(_mouse1);
	if _x > _maxX:
        	_maxX = _x;
	if _y > _maxY:
		 _maxY = _y;

	if (_countX > libraries.console.getTerminalSize()[0] - 5 | _countX < 5):
		exit();

	if abs(_deltaX) > _winScaleX:
        	#print("Draw X at (" + str(_countX) + "," + str(_countY) + ")");
		if (_deltaX > 0):
			window.addch(_countY, _countX, '>');
			_countX += 1;
		else:
			window.addch(_countY, _countX, '<');
                	_countX -= 1;
	
        	_deltaX = 0;
			
	else:
        	_deltaX += _x;

	if abs(_deltaY) > _winScaleY:
        	#print("Draw Y at (" + str(_countX) + "," + str(_countY) + ")");
		if (_deltaY > 0):
                	window.addch(_countY, _countX, '^');
                	_countY -= 1;
        	else:
                	window.addch(_countY, _countX, 'v');
                	_countY += 1;

        	_deltaY = 0;

	else:
        	_deltaY += _y;


	window.refresh();


file.close();
curses.endwin();
