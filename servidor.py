#
# servidor.py
# Autor: Misael Saenz Flores
# Version: 13/10/2016
#
import sys
import uuid
import random
from PyQt4 import QtCore, QtGui, uic
from xmlrpc.server import SimpleXMLRPCServer

w = uic.loadUiType("servidor.ui")[0]

class VentanaServidor(QtGui.QWidget, w):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.setupUi(self)
		self.timer_estado = None
		self.timer_servidor = None
		self.pushButton_iniciar_servidor.clicked.connect(self.IniciarServidor)
		self.spinBox_espera.valueChanged.connect(self.CambiaTiempo)
		self.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
		self.tableWidget.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
		self.tableWidget.keyPressEvent = self.keyPressEventTable
		self.tableWidget.setSelectionMode(QtGui.QTableWidget.NoSelection)
		self.spinBox_columnas.valueChanged.connect(self.CambiarColumnas)
		self.spinBox_filas.valueChanged.connect(self.CambiarFilas)
		self.pushButton_terminar_juego.setVisible(False)
		self.pushButton_iniciar_juego.setCheckable(True)
		self.pushButton_iniciar_juego.clicked.connect(self.IniciarJuego)
		self.pushButton_terminar_juego.clicked.connect(self.TerminarJuego)
		self.AgrgarItem()
		self.show()

	def CambiarColumnas(self):
		self.tableWidget.setColumnCount(self.spinBox_columnas.value())
		self.AgrgarItem()
	
	def CambiarFilas(self):
		self.tableWidget.setRowCount(self.spinBox_filas.value())
		self.AgrgarItem()

	def IniciarJuego(self):
		if self.pushButton_iniciar_juego.isChecked():
			self.snake = Snake()
			print(Snake().ID)
			self.timer_estado = QtCore.QTimer(self)
			self.timer_estado.timeout.connect(self.MoverSnake)
			self.timer_estado.start(250)
			self.tableWidget.installEventFilter(self)
			self.pushButton_terminar_juego.setVisible(True)
			self.pushButton_iniciar_juego.setText("Pausar el Juego")
			for x in range(self.snake.Tam()):
				i = self.snake.Cuerpo[x]
				j = self.tableWidget.itemAt(i[0],i[1])
				self.tableWidget.item(i[0],i[1]).setBackground(QtGui.QColor(254,000,000))
		else:
			self.pushButton_iniciar_juego.setText("Reanudar Juego")

	def TerminarJuego(self):
		if self.pushButton_iniciar_juego.isChecked():
			self.timer_estado.stop()
			self.snake = None
			self.pushButton_iniciar_juego.setCheckable(False)
			self.pushButton_iniciar_juego.setCheckable(True)
			self.pushButton_iniciar_juego.setText("Iniciar Juego")
			self.pushButton_terminar_juego.setVisible(False)
			self.AgrgarItem()


	def MoverSnake(self):
		x = self.snake.Cuerpo[0]
		y = self.snake.Cuerpo[-1]
		t = [y[0],y[1]]
		if self.pushButton_iniciar_juego.isChecked():
			if self.snake.Direccion == "AR":
				z = (x[0] - 1) % self.tableWidget.rowCount()
				self.snake.Camino.append((z,x[1]))
				self.snake.Cuerpo.insert(0,[z,x[1]])
				l = [z,x[1]]
				try:
					self.AgregarItemTable(t,l)
				except:
					pass
				del self.snake.Cuerpo[-1]
			elif self.snake.Direccion == "AB":
				z = (x[0] + 1) % self.tableWidget.rowCount()
				self.snake.Camino.append((z,x[1]))
				self.snake.Cuerpo.insert(0,[z,x[1]])
				l = [z,x[1]]
				try:
					self.AgregarItemTable(t,l)
				except:
					pass
				del self.snake.Cuerpo[-1]
			elif self.snake.Direccion == "D":
				z = (x[1] + 1) % self.tableWidget.columnCount()
				self.snake.Camino.append((x[0],z))
				self.snake.Cuerpo.insert(0,[x[0],z])
				l = [x[0],z]
				try:
					self.AgregarItemTable(t,l)
				except:
					pass
				del self.snake.Cuerpo[-1]
			elif self.snake.Direccion == "I":
				z = (x[1] - 1) % self.tableWidget.columnCount()
				self.snake.Camino.append((x[0],z))
				self.snake.Cuerpo.insert(0,[x[0],z])
				l = [x[0],z]
				try:
					self.AgregarItemTable(t,l)
				except:
					pass
				del self.snake.Cuerpo[-1]
			if (self.snake.Cuerpo[0] in self.snake.Cuerpo[1:self.snake.Tam()]):
				self.TerminarJuego()
				print("Muere")

	def CambiaTiempo(self):
		self.timer_estado.setInterval(self.spinBox_espera.value())

	def keyPressEventTable(self, event):
		key = event.key()
		if key == QtCore.Qt.Key_Up:
			self.snake.Cdireccion("AR")
		elif key == QtCore.Qt.Key_Down:
			self.snake.Cdireccion("AB")
		elif key == QtCore.Qt.Key_Left:
			self.snake.Cdireccion("I")
		elif key == QtCore.Qt.Key_Right:
			self.snake.Cdireccion("D")

	def AgrgarItem(self):
		for i in range(self.tableWidget.rowCount()):
			for j in range(self.tableWidget.columnCount()):
				self.tableWidget.setItem(i,j, QtGui.QTableWidgetItem())
				self.tableWidget.item(i,j).setBackground(QtGui.QColor(255,255,255))

	def AgregarItemTable(self, x,y):
		self.tableWidget.setItem(x[0],x[1], QtGui.QTableWidgetItem())
		self.tableWidget.item(x[0],x[1]).setBackground(QtGui.QColor(255,255,255))
		self.tableWidget.setItem(y[0],y[1], QtGui.QTableWidgetItem())
		self.tableWidget.item(y[0],y[1]).setBackground(QtGui.QColor(Snake().rojo,Snake().verde,Snake().azul))

	def IniciarServidor(self):
		puerto = self.spinBox_puerto.value()
		if puerto == 0:
			puerto = 8000
		ip = str(self.lineEdit_url.text())
		self.Servidor = SimpleXMLRPCServer((ip,puerto), allow_none = True)
		self.spinBox_puerto.setValue(puerto)
		self.Servidor.timeout = self.doubleSpinBox_timeout.value()
		self.doubleSpinBox_timeout.setValue(self.Servidor.timeout)
		self.doubleSpinBox_timeout.setReadOnly(True)
		self.spinBox_puerto.setReadOnly(True)
		self.timer_servidor = QtCore.QTimer()
		self.timer_servidor.timeout.connect(self.timepoConexion)
		self.Servidor.register_function(self.ping)
		self.Servidor.register_function(self.yo_juego)
		self.Servidor.register_function(self.cambia_direccion)
		self.Servidor.register_function(self.estado_del_juego)
		self.timer_servidor.start(100)

	def timepoConexion(self):
		self.Servidor.handle_request()

	def  cambia_direccion(self, identidad, n):
		if(self.snake.ID == identidad):
			if(n == 0):
				self.snake.Cdireccion("AR")
			if(n == 1):
				self.snake.Cdireccion("D")
			if(n == 2):
				self.snake.Cdireccion("AB")
			if(n == 3):
				self.snake.Cdireccion("I")

	def yo_juego(self):
		self.tableWidget.clear()
		self.snake = Snake()
		est = {'ID': Snake().ID, 'Color': Snake().Color}
		for x in Snake().Cuerpo:
			self.tableWidget.setItem(x[0],x[1], QtGui.QTableWidgetItem())
			self.tableWidget.item(x[0],x[1]).setBackground(QtGui.QColor(Snake().rojo,Snake().verde,Snake().azul))
		return est

	def ping(self):
		return "¡Pong!"

	def estado_del_juego(self):
		estado_juego = dict()
		estado_juego = {'espera': self.Servidor.timeout, 'tamX': self.tableWidget.columnCount(), 'tamY': self.tableWidget.rowCount(), 'vivoras': self.snake.DatosSnake()}
		return estado_juego

class Snake():
	def __init__(self):
		self.ID = str(uuid.uuid4())[9:13]
		self.Cuerpo = [[5,0],[4,0],[3,0],[2,0],[1,0],[0,0]]
		self.Direccion = "AB"
		self.Camino = []
		self.rojo = int(random.uniform(0,255))
		self.verde = int(random.uniform(0,255))
		self.azul = int(random.uniform(0,255))
		self.Color = {'r': self.rojo, 'g': self.verde, 'b': self.azul}

	def Id(self):
		return self.ID

	def DatosSnake(self):
		estado = {'ID': self.ID, 'Camino': self.Camino, 'Color': self.Color}
		return estado

	def Tam(self):
		return len(self.Cuerpo)

	def Cdireccion(self, direccion):
		self.Direccion = direccion

	def Muere(self):
		if (self.Cuerpo[0] in self.Cuerpo[0:]):
			return True
		else:
			return False

app = QtGui.QApplication(sys.argv)
MiVentana = VentanaServidor(None)
MiVentana.show()
app.exec_()