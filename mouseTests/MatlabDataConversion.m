function[delXr, delYr, delOmeg] = MatlabDataConversion(theta1, phi1, theta2, phi2, x1,y1, x2, y2)
[theta1, phi1, theta2, phi2] = radians(theta1, phi1, theta2, phi2); 
r1 = 4;
r2 = 4;
alpha1 = theta1 + phi1;
alpha2 = theta2 + phi2; 

delXr1 = [sin(alpha1) -cos(alpha1) r1*cos(phi1)]; %equation in the x direction for mouse 1
delYr1 = [cos(alpha1) sin(alpha1) r1*sin(phi1)];%equation in y direction for mouse 1

delXr2 = [sin(alpha2) -cos(alpha2) r2*cos(phi2)];
delYr2 = [cos(alpha2) sin(alpha2) r2*sin(phi2)]; 


A = [delXr1; delYr1; delXr2; delYr2] %matrix for 2 mice

%Atransp = transpose(A); 
%invA = inv(a); 
%pInvA is the pseudoinverse

%pInvA = Atransp / (A*Atransp); 

pInvA = pinv(A);

%x1, x2, y1, y2 are the sensor measurements
motionCoefs = pInvA * [x1; y1; x2; y2]; 

delXr = motionCoefs(1)
delYr = motionCoefs(2)
delOmeg = motionCoefs(3)
end

function [theta1, phi1, theta2, phi2] = radians(theta1, phi1, theta2, phi2)

theta1 = theta1.*pi./180; 
phi1 = phi1.*pi./180; 
theta2 = theta2.*pi./180; 
phi2= phi2.*pi./180; 
end
