# pyuic4 -o ui_mainwindow.py IEEESim.ui (to compile Qt designer file into python object)
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_mainwindow
import socket
import sys
import numpy
from math import *

HOST = '' # recieving
PORT = 8888
TESTING = True # if True, data input is printed to console
ISGAMELEFT = False

xw = 0.0 if ISGAMELEFT else 96.0 # data passed from robot remotely
yw = 0.0
heading = 0.0
_scale = 15 # 1 inch is represented as 15 pixels
_robotsize = 11.5 * _scale # robot size in inches
_size = 96 * _scale # size of the GUI window



# game board elements
startArea = ((0,0),(0,30),(20,30),(20,0),(0,0)) if ISGAMELEFT else ((96,0),(96,30),(76,30),(76,0),(96,0))
tunnel = ((0,30),(0,45),(18,45),(18,30),(0,30)) if ISGAMELEFT else ((96,30),(96,45),(78,45),(78,30),(96,30))
truck = ((20,0),(20,12),(30,12),(30,0),(20,0)) if ISGAMELEFT else ((76,0),(76,12),(66,12),(66,0),(76,0))
boat = ((60,0),(60,24),(96,24),(96,0),(60,0)) if ISGAMELEFT else ((36,0),(36,24),(0,24),(0,0),(36,0))
loadingC = ((10,79),(10,84),(25,84),(25,79),(10,79)) if ISGAMELEFT else ((86,79),(86,84),(71,84),(71,79),(86,79))
loadingB = ((40,79),(40,84),(55,84),(55,79),(40,79)) if ISGAMELEFT else ((56,79),(56,84),(41,84),(41,79),(56,79))
loadingA = ((65,79),(65,84),(80,84),(80,79),(65,79)) if ISGAMELEFT else ((31,79),(31,84),(16,84),(16,79),(31,79))
center = ((43.5,46.5),(43.5,49.5),(51.5,49.5),(51.5,46.5),(43.5,46.5))
box1 = ((85,69),(85,80),(93,80),(93,69),(85,69)) if ISGAMELEFT else ((11,69),(11,80),(3,80),(3,69),(11,69))
box2 = ((85,57),(85,68),(93,68),(93,57),(85,57)) if ISGAMELEFT else ((11,57),(11,68),(3,68),(3,57),(11,57))
box3 = ((85,45),(85,56),(93,56),(93,45),(85,45)) if ISGAMELEFT else ((11,45),(11,56),(3,56),(3,45),(11,45))
box4 = ((85,33),(85,44),(93,44),(93,33),(85,33)) if ISGAMELEFT else ((11,33),(11,44),(3,44),(3,33),(11,33))
zoneA = ((64,84),(64,94),(96,94),(96,84),(64,84)) if ISGAMELEFT else ((32,84),(32,94),(0,94),(0,84),(32,84))
zoneB = ((32,84),(32,94),(64,94),(64,84),(32,84)) if ISGAMELEFT else ((64,84),(64,94),(32,94),(32,84),(64,84))
zoneC = ((0,84),(0,94),(32,94),(32,84),(0,84)) if ISGAMELEFT else ((96,84),(96,94),(64,94),(64,84),(96,84))
board = (startArea, tunnel, truck, boat, loadingA, loadingB, loadingC, center, box1, box2, box3, box4, zoneA, zoneB, zoneC)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
s.settimeout(0.001) # insanely fast timeout so we're basically constanly checking

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit() # todo, don't exit, retry?
print 'Socket now listening on port ' + str(PORT)

class MainWindow(QMainWindow, ui_mainwindow.Ui_MainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.setupUi(self)
		self.updateUi() # update the UI (generated code)
		self.installEventFilter(self) # add the eventFilter

	def eventFilter(self,target,event):
		global xw, yw
		if(event.type()==QEvent.MouseButtonPress): # if the mouse pressed somewhere on the GUI
			print "Moving robot to (", str(event.x()), ", ", event.y(), ")..."
			return True # handled
		else:
			return False # not handled

	def paintEvent(self, e): # draw the game board
		qp = QPainter()
		qp.begin(self)
		pen = QPen(Qt.black, 3, Qt.SolidLine)
		qp.setPen(pen)
		self.drawBoard(qp) # do the drawing (robot and obstacles)
		qp.end()

	def drawBoard(self, qp):
		global xw, yw, _scale, heading # need the position to draw the robot
		for area in range(0, len(board)): # for each obstacle
			for num in range(0, len(board[area])-1):
				qp.drawLine(board[area][num][0]*_scale, _size-board[area][num][1]*_scale, board[area][num+1][0]*_scale, _size-board[area][num+1][1]*_scale)
		qp.translate(xw*_scale, _size-yw*_scale) # move the painter to the center of the robot
		qp.rotate(heading) # now rotate it
		rect = QRectF() # create a rectangle, set it's width and height
		rect.setWidth(_robotsize)
		rect.setHeight(_robotsize)
		rect.moveCenter(QPointF(0.0, 0.0)) # since qp is translated to center of robot, make sure robot rectangle is centered at 0,0
		qp.drawRect(rect) # draw the robo
		qp.drawPie(rect, 20 * 16, 140 * 16); # draw the inside angle diagram to show front
		qp.translate(-(xw*_scale), -(_size-yw*_scale)) # translate it back to true 0,0 (top left corner

	def updateUi(self):
		global xw, yw, heading
		try:
			msg = eval(s.recv(100))
		except:
			e = sys.exc_info()
		else:
			xw=msg[0]
			yw=msg[1]
			heading=msg[2]
			if TESTING:
				print str((round(xw,2), round(yw,2), round(heading,4)))
		self.repaint() # repaint the robot
		QTimer.singleShot(1, self.updateUi) # infinite recursion

if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	form = MainWindow()
	form.show()
	app.exec_()
	s.close()
