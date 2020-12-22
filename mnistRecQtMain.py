from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, QHBoxLayout, QApplication, QVBoxLayout
from PyQt5.QtGui import QColor, QPainter, QBrush
from PyQt5.QtCore import Qt
import sys
import copy
import numpy as np
from test import Predict

__appname__ = 'MnistRec'

class PaintCanvas(QWidget):
	def __init__(self, *args, **kwargs):
		super(PaintCanvas, self).__init__(*args, **kwargs)
		self.setMouseTracking(True)
		self.drawingColor = QColor(0, 0, 0)
		self.pointsList = []
		self.painter = QPainter(self)
		self.tempPoints = []
		self.setFixedSize(28, 28)
		self.bDrawing = False

	def paintForEvent(self, ev):
		pos = ev.pos()
		window = self.parent().window()
		if window is not None:
			window.labelCoordinates.setText('x: %d, y: %d'%(pos.x(), pos.y()))
		# print(ev.button())
		if self.bDrawing or ev.button() == Qt.LeftButton:
			self.tempPoints.append((pos.x(), pos.y()))
			self.update()

	def mouseMoveEvent(self, ev):
		self.paintForEvent(ev)

	def mousePressEvent(self, ev):
		self.paintForEvent(ev)
		self.bDrawing = True

	def mouseReleaseEvent(self, ev):
		self.paintForEvent(ev)
		self.pointsList.append(copy.deepcopy(self.tempPoints))
		self.tempPoints.clear()
		self.bDrawing = False

	def paintEvent(self, ev):
		p = self.painter
		p.begin(self)
		p.setPen(self.drawingColor)
		brush = QBrush(Qt.BDiagPattern)
		p.setBrush(brush)
		# print(self.pointsList)
		# print(self.tempPoints)
		for points in self.pointsList:
			for i in range(len(points)-1):
				p.drawLine(points[i][0], points[i][1], points[i+1][0], points[i+1][1])
		for tPidx in range(len(self.tempPoints)-1):
			p. drawLine(self.tempPoints[tPidx][0], self.tempPoints[tPidx][1], self.tempPoints[tPidx+1][0], self.tempPoints[tPidx+1][1])
		p.end()

class MnistRecQtMain(QMainWindow):

	def __init__(self):
		super(MnistRecQtMain, self).__init__()
		# self.resize(800, 600)
		self.setWindowTitle(__appname__)
		self.paintCanvas = PaintCanvas(parent=self)
		self.recButton = QPushButton('Recognize')
		self.recButton.clicked.connect(self.recognize)
		self.cleanButton = QPushButton('Clean')
		self.cleanButton.clicked.connect(self.cleanCanvas)
		self.digitLabel = QLabel('')
		layout = QHBoxLayout()
		layout.addWidget(self.paintCanvas)
		buttonLayout = QVBoxLayout()
		buttonLayout.addWidget(self.recButton)
		buttonLayout.addWidget(self.cleanButton)
		layout.addLayout(buttonLayout)
		layout.addWidget(self.digitLabel)
		centralWidget = QWidget()
		centralWidget.setLayout(layout)
		self.setCentralWidget(centralWidget)
		self.statusBar().showMessage('%s started.'%__appname__)
		self.statusBar().show()
		self.labelCoordinates = QLabel('')
		self.statusBar().addPermanentWidget(self.labelCoordinates)
		self.predict = Predict()

	def recognize(self):
		img = np.ones((28, 28))
		for points in self.paintCanvas.pointsList:
			for point in points:
				img[point[0], point[1]] = 0
		img = np.reshape(img, (28, 28, 1))
		self.digitLabel.setText(str(self.predict.predict_img(img)))

	def cleanCanvas(self):
		self.paintCanvas.pointsList.clear()
		self.paintCanvas.update()

def get_main_app(argv=[]):
	app = QApplication(argv)
	app.setApplicationName(__appname__)
	win = MnistRecQtMain()
	win.show()
	return app, win

app, _win = get_main_app(sys.argv)
sys.exit(app.exec_())