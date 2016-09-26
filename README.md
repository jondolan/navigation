Georgia Tech IEEE Hardware Team

Software for the 2015-2016 competition year navigation subteam. Competition details can be found at http://sites.ieee.org/southeastcon2016/student-program/ under hardware competition.

The autonomous navigation was based off of 2 optical mice mounted on custom 3D printed sleds on opposite sides of the robot. These mice each provided (x, y) translation pairs, which were then transformed into a (x, y, theta) for the robot coordinate reference frame. Dead reckoning was preformed to turn initially relative mouse movements into absolute units, usable for game board tracking.

![Mouse Optical Mouse](/mousemount.jpg?raw=true "Mouse Optical Mouse")

Simulation software was developed to visualize the movement of the robot around the game board.

![Simulation GUI Window](/simulationscreenshot.jpg?raw=true "Simulation GUI Window")

The simulation software can be run in different modes. "pathplanner.py" shows a basic implementation of our navigation algorithm running on the GUI via python web sockets (shown below in the animated image). "client.py" is designed to be run on a BeagleBone Black connected to a host computer for simulation purposes, taking in and sending the raw data back to the computer to then display on the GUI.

![pathplanner.py simulation](/simulation.gif?raw=true "pathplanner.py simulation")
