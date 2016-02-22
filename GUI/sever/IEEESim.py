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

startArea = ((0,0), (0,300), (200,300), (200,0))

 
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

	def paintEvent(self, e):
		qp = QPainter()
		qp.begin(self)
		self.drawBoard(qp)
		qp.end()

	def drawBoard(self, qp):
		pen = QPen(Qt.black, 2, Qt.SolidLine)
		qp.setPen(pen)
		for num in range(0, len(startArea)-1):
			qp.drawLine(startArea[num][0], 960-startArea[num][1], startArea[num+1][0], 960-startArea[num+1][1])

	def updateUi(self):
		global _deltaX, _deltaY, _increment
		print str(self.centralwidget.height)
		try:
			msg = eval(s.recv(14))
		except:
			e = sys.exc_info()
#			print sys.exc_info()
		else:
			_deltaX+=msg[0]
			_deltaY+=msg[1]
			self.label.setGeometry(QRect(_deltaX/_dotsPerInch, 900-(_deltaY/_dotsPerInch), 50, 40))
#			self.label.setGeometry(QRect(_deltaX, 900-(_deltaY), 20, 20))
#			_increment+=1
		QTimer.singleShot(1, self.updateUi)

if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	form = MainWindow()
	form.show()
	app.exec_()
	s.close()
