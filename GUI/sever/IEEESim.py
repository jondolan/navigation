# pyuic4 -o ui_mainwindow.py IEEESim.ui (to compile Qt designer file into python object)
import re
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_mainwindow
import socket
import sys

HOST = ''
PORT = 8888
_deltaX = 0
_deltaY = 0
_dotsPerInch = 184.8375
_increment = 0
_scale = 15
_size = 96 * _scale

startArea = ((0,0),(0,30),(20,30),(20,0),(0,0))
tunnel = ((0,30),(0,45),(18,45),(18,30),(0,30))
truck = ((20,0),(20,12),(30,12),(30,0),(20,0))
boat = ((60,0),(60,24),(96,24),(96,0),(60,0))
loadingC = ((10,79),(10,84),(25,84),(25,79),(10,79))
loadingB = ((40,79),(40,84),(55,84),(55,79),(40,79))
loadingA = ((65,79),(65,84),(80,84),(80,79),(65,79))
center = ((43.5,46.5),(43.5,49.5),(51.5,49.5),(51.5,46.5),(43.5,46.5))
box1 = ((85,69),(85,80),(93,80),(93,69),(85,69))
box2 = ((85,57),(85,68),(93,68),(93,57),(85,57))
box3 = ((85,45),(85,56),(93,56),(93,45),(85,45))
box4 = ((85,33),(85,44),(93,44),(93,33),(85,33))
areaA = ((0,84),(0,94),(32,94),(32,84),(0,84))
areaB = ((32,84),(32,94),(64,94),(64,84),(32,84))
areaC = ((64,84),(64,94),(96,94),(96,84),(64,84))

board = (startArea, tunnel, truck, boat, loadingA, loadingB, loadingC, center, box1, box2, box3, box4, areaA, areaB, areaC)
		 

 
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(0.001)

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     

print 'Socket now listening on port ' + str(PORT)
 

class MainWindow(QMainWindow, ui_mainwindow.Ui_MainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.setupUi(self)
		self.updateUi()
		self.label.setGeometry(QRect(0, _size-40, 50, 40))
		self.installEventFilter(self)

	def eventFilter(self,target,event):
		global _deltaX, _deltaY
		if(event.type()==QEvent.MouseButtonPress):
			_deltaX, _deltaY = event.x()*_dotsPerInch, (_size-event.y())*_dotsPerInch
			self.updateUi()
			print "Moving robot to (", str(event.x()), ", ", event.y(), ")..."
			return True
		else:
			return False

	def paintEvent(self, e):
		qp = QPainter()
		qp.begin(self)
		self.drawBoard(qp)
		qp.end()

	def drawBoard(self, qp):
		pen = QPen(Qt.black, 2, Qt.SolidLine)
		qp.setPen(pen)
		for area in range(0, len(board)):
			for num in range(0, len(board[area])-1):
				qp.drawLine(board[area][num][0]*_scale, _size-board[area][num][1]*_scale, board[area][num+1][0]*_scale, _size-board[area][num+1][1]*_scale)

	def updateUi(self):
		global _deltaX, _deltaY, _increment
		try:
			msg = eval(s.recv(14))
		except:
			e = sys.exc_info()
#			print sys.exc_info()
		else:
			_deltaX+=msg[0]
			_deltaY+=msg[1]
#			_increment+=1
		self.label.setGeometry(QRect(_deltaX/_dotsPerInch, _size-40-(_deltaY/_dotsPerInch), 50, 40))
		print _deltaX
		QTimer.singleShot(1, self.updateUi)

if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	form = MainWindow()
	form.show()
	app.exec_()
	s.close()
