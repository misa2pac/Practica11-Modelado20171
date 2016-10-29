import sys
from PyQt4 import QtCore, QtGui, uic
from xmlrpc.client import ServerProxy

w = uic.loadUiType("cliente.ui")[0]

class VentanaCliente(QtGui.QWidget, w):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.setupUi(self)
		self.estado = None
		self.vivora = None
		self.timer_estado = QtCore.QTimer()
		self.timer_estado.timeout.connect(self.Actualizar)
		self.tableWidget.keyPressEvent = self.keyPressEventTable
		self.tableWidget.horizontalHeader().hide()
		self.tableWidget.verticalHeader().hide()
		self.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
		self.tableWidget.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
		self.pushButton_ping.clicked.connect(self.Ping)
		self.pushButton_participar.clicked.connect(self.IniciarJuego)
		self.lineEdit_id.setReadOnly(True)
		self.lineEdit_color.setReadOnly(True)

	def Ping(self):
		self.pushButton_ping.setText("Pinging...")
		try:
			self.url = 'http://' + str(self.lineEdit_url.text()) + ':' + str(self.spinBox_puerto.value())
			self.cliente = ServerProxy(self.url)
			self.pushButton_ping.setText(self.cliente.ping())
		except:
			self.pushButton_ping.setText("No pong :(")

	def IniciarJuego(self):
		self.url = 'http://' + str(self.lineEdit_url.text()) + ':' + str(self.spinBox_puerto.value())
		self.cliente = ServerProxy(self.url)
		try:
			self.vivora = self.cliente.yo_juego()
			self.estado = self.cliente.estado_del_juego()
		except:
			print("no hay conexion")
		self.columnas = self.estado['tamX']
		self.filas = self.estado['tamY']
		self.tableWidget.setRowCount(self.filas)
		self.tableWidget.setColumnCount(self.columnas)
		self.lineEdit_id.setText(str(self.vivora['ID']))
		self.lineEdit_color.setText(str(self.vivora['Color']))
		self.pushButton_participar.setVisible(False)
		self.timer_estado.start(self.estado['espera'])
		self.vivora = self.estado['vivoras']

	def keyPressEventTable(self, event):
		key = event.key()
		if key == QtCore.Qt.Key_Up:
			self.dir = 0
			self.cliente.cambia_direccion(self.vivora['ID'],self.dir)
		elif key == QtCore.Qt.Key_Down:
			self.dir = 2
			self.cliente.cambia_direccion(self.vivora['ID'],self.dir)
		elif key == QtCore.Qt.Key_Left:
			self.dir = 3
			self.cliente.cambia_direccion(self.vivora['ID'],self.dir)
		elif key == QtCore.Qt.Key_Right:
			self.dir = 1
			self.cliente.cambia_direccion(self.vivora['ID'],self.dir)

	def Actualizar(self):
		self.tableWidget.clear()
		self.estado = self.cliente.estado_del_juego()
		if(self.estado['tamY'] != self.filas or self.estado['tamX'] != self.columnas):
			self.filas = self.estado['tamY']
			self.columnas = self.estado['tamX']
			self.tableWidget.setRowCount(self.filas)
			self.tableWidget.setColumnCount(self.columnas)
		self.vivora= self.estado['vivoras']
		self.Cuerpo = self.vivora['Camino']
		self.Color = self.vivora['Color']
		for x in self.Cuerpo:
			self.tableWidget.setItem(x[0],x[1], QtGui.QTableWidgetItem())
			self.tableWidget.item(x[0],x[1]).setBackground(QtGui.QColor(self.Color['r'],self.Color['g'],self.Color['b']))

app = QtGui.QApplication(sys.argv)
MiVentana = VentanaCliente(None)
MiVentana.show()
app.exec_()