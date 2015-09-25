import struct
import time

file = open( "/dev/input/mice", "rb" );

start_time = time.time();
clicksX = 0;
clicksY = 0;

def getMouseEvent():
  global clicksX, clicksY;
  buf = file.read(3); # read in from /dev/input/mice
  button = ord( buf[0] ); # changes this into an understandable number - 1 = left button, 2 = right button, 4 = middle button, etc
  #print(button)
  bLeft = button & 0x1;
  bMiddle = ( button & 0x4 ) > 0;
  bRight = ( button & 0x2 ) > 0;
  x,y = struct.unpack( "bb", buf[1:] );
  clicksX += x;
  clicksY += y;
  # return stuffs

while( 1 ):
  start_time_loop = time.time();
  getMouseEvent();
  #print(time.time() - start_time_loop);
  print ("Total x: %d, y: %d\n" % (clicksX, clicksY) );
file.close();
