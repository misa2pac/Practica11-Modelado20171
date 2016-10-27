import sys
from PyQt4 import QtCore, QtGui, uic

w = uic.loadUiType("cliente.ui")[0]

class VentanaCliente(QtGui.QWidget, w):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.setupUi(self)
		self.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
		self.tableWidget.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

app = QtGui.QApplication(sys.argv)
MiVentana = VentanaCliente(None)
MiVentana.show()
app.exec_()