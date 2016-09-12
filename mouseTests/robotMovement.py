# In [7], several assumptions are made about the characteristics of the mouse sensors which are used to detect and
# correct for errors. In general, mouse sensors do not measure a distance greater than the actual distance traveled. The
# optical flow algorithm may miss counts due to poor focus or insufficient frame overlap, but it will not overestimate
# the motion. Thus, when there is disagreement between one or more sensors, the sensor with the higher measurement
# is probably correct.


# import libraries
#import mouse
# library for retreiving mouse data
import struct
from math import *
import numpy
from scipy import linalg

# read mouse movement from file
def getMouseMovement(mouse):
	_fIn = mouse.read(3);
	return struct.unpack("bb", _fIn[1:]);


# global variables
_mouse0 = open( "/dev/input/mouse0", "rb" );	#open mouse on top right
_mouse1 = open( "/dev/input/mouse1", "rb" );	#open mouse on top left

theta0 = 45;
phi0 = 45;		
theta1 = -45;
phi1 = 45;
r0 = 4;
r1 = 4;
alpha0 = theta0 + phi0;
alpha1 = theta1 + phi1; 

A = [[sin(alpha0), -cos(alpha0), r0*cos(phi0)],
	[cos(alpha0), sin(alpha0), r0*sin(phi0)],
	[sin(alpha1), -cos(alpha1), r1*cos(phi1)],
	[cos(alpha1), sin(alpha1), r1*sin(phi1)]
	];

pInvA = linalg.pinv(A)

_x0 = 0;
_y0 = 0;
_x1 = 0;
_y1 = 0;
_deltaX = 0;
_deltaY = 0;
_deltaW = 0;
_dotsPerInch = 1848.375;

#fOut = open('movement.txt', 'w');


while (1):
	#Refresh Data
	x0, y0 = getMouseMovement(_mouse0);
	x1, y1 = getMouseMovement(_mouse1);
	
	_x0 += x0;
	_x1 += x1;
	
	changeArray = numpy.dot(pInvA, [[x0], [y0], [x1], [y1]]);

	_deltaX += changeArray [0,0];
	_deltaY += changeArray [1,0];
	_deltaW += changeArray [2,0];
	#print("Inches: " + str(sqrt((_deltaX**2) + (_deltaY**2))/_dotsPerInch) + "\n");
	print("Dots: (" + str(_deltaX) + "," + str(_deltaY) + ")\nInches: (" + str(_deltaX/_dotsPerInch) + "," + str(_deltaY/_dotsPerInch) + ")\n");
	print("Dots: m0 (" + str(_x0) + "," + str(_y0) + ")  m1 (" + str(_x1) + "," + str(_y1) + ")\n");
	
#fOut.close();
