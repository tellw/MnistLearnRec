from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, QHBoxLayout, QApplication
from PyQt5.QtGui import QColor, QPainter, QBrush
from PyQt5.QtCore import Qt
import sys

__appname__ = 'MnistRec'

class PaintCanvas(QWidget):
	def __init__(self, *args, **kwargs):
		super(PaintCanvas, self).__init__(*args, **kwargs)
		self.setMouseTracking(True)
		self.drawingColor = QColor(0, 0, 0)
		self.pointsList = []
		self.painter = QPainter(self)
		self.tempPoints = []

	def paintForEvent(self, ev):
		pos = ev.pos()
		window = self.parent().window()
		if window is not None:
			window.labelCoordinates.setText('x: %d, y: %d'%(pos.x(), pos.y()))
		if ev.button() == Qt.LeftButton:
			self.tempPoints.append((pos.x(), pos.y()))
			self.update()

	def mouseMoveEvent(self, ev):
		self.paintForEvent(ev)

	def mousePressEvent(self, ev):
		self.paintForEvent(ev)

	def mouseReleaseEvent(self, ev):
		self.paintForEvent(ev)
		self.pointsList.append(self.tempPoints)
		self.tempPoints.clear()

	def paintEvent(self, ev):
		p = self.painter
		p.begin(self)
		p.setPen(self.drawingColor)
		for points in self.pointsList:
			for i in range(len(points)-1):
				p.drawLine(points[i][0], points[i][1], points[i+1][0], points[i+1][1]);
		for tPidx in range(len(self.tempPoints)-1):
			p. drawLine(self.tempPoints[tPidx][0], self.tempPoints[tPidx][1], self.tempPoints[tPidx+1][0], self.tempPoints[tPidx+1][1])
		p.end()
class MnistRecQtMain(QMainWindow):

	def __init__(self):
		super(MnistRecQtMain, self).__init__()
		self.resize(800, 600)
		self.setWindowTitle(__appname__)
		self.paintCanvas = PaintCanvas(parent=self)
		self.recButton = QPushButton('Recognize')
		self.recButton.clicked.connect(self.recognize)
		self.digitLabel = QLabel('')
		layout = QHBoxLayout()
		layout.addWidget(self.paintCanvas)
		layout.addWidget(self.recButton)
		layout.addWidget(self.digitLabel)
		centralWidget = QWidget()
		centralWidget.setLayout(layout)
		self.setCentralWidget(centralWidget)
		self.statusBar().showMessage('%s started.'%__appname__)
		self.statusBar.show()
		self.labelCoordinates = QLabel('')
		self.statusBar().addPermanentWidget(self.labelCoordinates)

	def recognize(self):
		pass

def get_main_app(argv=[]):
	app = QApplication(argv)
	app.setApplicationName(__appname__)
	win = MnistRecQtMain()
	win.show()
	return app, win

app, _win = get_main_app(sys.argv)
sys.exit(app.exec_())