import math;
import numpy;

def miceCoeff(theta1, phi1, theta2, phi2, x1, y1, x2, y2):
	
	theta1 = math.radians(theta1)
	theta2 = math.radians(theta2)
	phi1 = math.radians(phi1)
	phi2 = math.radians(phi2)

	r1 = 4
	r2 = 4
	alpha1 = theta1 + phi1
	alpha2 = theta2 + phi2;

	delXr1 = [math.sin(alpha1), -math.cos(alpha1), r1*math.cos(phi1)] #equation in the x direction for mouse 1
	delYr1 = [math.cos(alpha1), math.sin(alpha1), r1*math.sin(phi1)] #equation in y direction for mouse 1

	delXr2 = [math.sin(alpha2), -math.cos(alpha2), r2*math.cos(phi2)]
	delYr2 = [math.cos(alpha2), math.sin(alpha2), r2*math.sin(phi2)]


	A = [delXr1, delYr1, delXr2, delYr2] #matrix for 2 mice
	pInvA = numpy.linalg.pinv(A)

	#x1, x2, y1, y2 are the sensor measurements
	motionCoefs = numpy.dot(pInvA, [x1, y1, x2, y2]);

	delXr = motionCoefs[0]
	delYr = motionCoefs[1]
	delOmeg = motionCoefs[2]

	return [delXr, delYr, delOmeg]

print miceCoeff(50, 50, 50, 50, 50, 50, 50, 50) # test case 1