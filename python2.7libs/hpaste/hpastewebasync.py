import hpasteweb as hw

try:
	from PySide2 import QtCore as qtc
	from PySide2.QtWidgets import *
	from PySide2.QtGui import *
except:
	try:
		from PySide import QtCore as qtc
		from PySide.QtGui import *
	except:
		raise RuntimeError("cannot load any PySide")

class SendThread(QThread):
	def __init__(self,parent=None):
		self.__asciiData=""

	def setInitData(self,data):
		self.__asciiData=data
	def run(self):
		hw.webPack(self.__asciiData)

class SenderWidget():
	class __SenderWidget(QWidget):
		class SenderState:
			idle=0
			sending=1
			finishing=2

			def __init__(self):
				raise RuntimeError("Don't instance this!")

		def __init__(self,parent=None):
			super(QWidget,self).__init__(parent)
			self.__workThread=None
			self.__state=self.SenderState.idle

		def send(self,asciiData):
			if(self.__workThread is not None):
				raise RuntimeError("Sender is already sending!")
			self.show()
			#TODO: move him to proper place
			self.__workThread=SendThread(self)
			self.__workThread.setInitData(asciiData)
			self.finished.connect(self.onFinish)

		def onFinish(self):
			self.__workThread.setParent(None)
			self.__workThread.deleteLater() #just to be sure
			self.__workThread=None

	_instance=None

	def __init__(self):
		if(SenderWidget._instance is None):
			SenderWidget._instance=SenderWidget.__SenderWidget()

	def __getattr__(self,item):
		return getattr(SenderWidget._instance, item)
