from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtCore import Qt

__appname__ = 'MnistRec'

class PaintCanvas(QWidget):
	def __init__(self, *args, **kwargs):
		super(PaintCanvas, self).__init__(*args, **kwargs)
		self.setMouseTracking(True)
		self.drawingColor = QColor(0, 0, 0)
		self.pointsList = []
		self.painter = QPainter(self)
		self.tempPoints = []

	def mouseMoveEvent(self, ev):
		pos = ev.pos()
		window = self.parent().window()
		if window is not None:
			self.parent().window().labelCoordinates.setText('x: %d, y: %d'%(pos.x(), pos.y()))
		if ev.button() == Qt.LeftButton:
			self.tempPoints.append((pos.x(), pos.y()))
			self.update


class MnistRecQtMain(QMainWindow):

	def __init__(self):
		super(MnistRecQtMain, self).__init__()
		self.resize(800, 600)
		self.setWindowTitle(__appname__)
		self.paintCanvas = PaintCanvas(parent=self)