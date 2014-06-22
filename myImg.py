#! /usr/bin/env env

from PySide import QtCore, QtGui
import ExtendedQLabel
import teste
import os

class Ui_Form(QtGui.QMainWindow):

	def __init__(self):
		self.path = os.getcwd() + '/c060/'
		print(self.path)
		self.manga = 'berserk'
		print(self.manga)
		self.page = 0
		self.scaleFactor = 1.0
		super(Ui_Form, self).__init__()
		self.setupUi(self)
		
		
	def setupUi(self, Form):
		
		Form.setObjectName("Form")
		Form.resize(1366, 768)
		
		self.imageLabel = ExtendedQLabel.ExtendedQLabel(Form)
		self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
		#self.imageLabel.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
		self.imageLabel.setScaledContents(True)
		self.imageLabel.setText("")
		self.imageLabel.setObjectName("imageLabel")

		#image clicked()
		self.connect(self.imageLabel, QtCore.SIGNAL('clicked()'), self.nextPage)

		self.scrollArea = QtGui.QScrollArea()
		
		#self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
		# collor black
		palette = QtGui.QPalette()
		brush = QtGui.QBrush(QtGui.QColor(24, 24, 24))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
		self.scrollArea.setPalette(palette)
		
		self.scrollArea.setGeometry(QtCore.QRect(560, 70, 201, 571))
		self.scrollArea.setWidget(self.imageLabel)
		self.scrollArea.setAlignment(QtCore.Qt.AlignCenter)
		self.setCentralWidget(self.scrollArea)
		
	
		self.pushButton = QtGui.QPushButton(Form)
		self.pushButton.setGeometry(QtCore.QRect(0, 0, 31, 31))
		self.pushButton.setObjectName("pushButton")            

		self.widget = QtGui.QWidget(Form)
		self.widget.setGeometry(QtCore.QRect(0, 0, 1366, 768))
		self.verticalLayout = QtGui.QVBoxLayout(self.widget)
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout.addWidget(self.pushButton)
		self.verticalLayout.addWidget(self.scrollArea)
			
		self.createActions()
		self.createMenus()
		
		self.updateActions()

		self.retranslateUi(Form)

		QtCore.QMetaObject.connectSlotsByName(Form)

	def retranslateUi(self, Form):
		Form.setWindowTitle(QtGui.QApplication.translate("Form", "Mangax", None, QtGui.QApplication.UnicodeUTF8))
		page = self.path + '000.jpg'
		self.strPage = page
		print(page)
		self.imageLabel.setPixmap(QtGui.QPixmap(page))
		self.imageLabel.adjustSize()

	def fitToWindow(self):
		fitToWindow = self.fitToWindowAct.isChecked()
		self.scrollArea.setWidgetResizable(fitToWindow)
		if not fitToWindow:
			self.normalSize()
		self.updateActions()
	
	def nextPage(self):

		# reset verticalscrollbar's position when the page is changed
		self.scrollArea.verticalScrollBar().setValue(0)
		# reset horizontalscrollbar's position when the page is changed
		self.scrollArea.horizontalScrollBar().setValue(0)

		# handling zoom
		self.scaleFactor = 1.0

		# handling pages
		self.page += 1		
		#print self.page

		if(self.page < 10):
			page = '00' + str(self.page)
		elif(10 <= self.page < 100):
			page = '0' + str(self.page)
		elif(self.page >= 100):
			page = str(self.page)
		page = self.path + page + '.jpg'
		self.strPage = page
		print (page)
		self.imageLabel.setPixmap(QtGui.QPixmap(page))
		self.imageLabel.adjustSize()
		
	def previusPage(self):

		#reset verticalscrollbar's position when the page is changed
		self.scrollArea.verticalScrollBar().setValue(0)
		# reset horizontalscrollbar's position when the page is changed
		self.scrollArea.horizontalScrollBar().setValue(0)

		# handling zoom
		self.scaleFactor = 1.0
		
		if(str(self.page) != "0"):
			self.page -= 1
			# handling pages
			#print self.page
			#page = str(self.page)
			if(self.page < 10):
				page = '00' + str(self.page)
			elif(10 <= self.page < 100):
				page = '0' + str(self.page)
			elif(self.page >= 100):
				page = str(self.page)
			
			page = self.path + page + '.jpg'
			self.strPage = page
			print (page)
			self.imageLabel.setPixmap(QtGui.QPixmap(page))
			self.imageLabel.adjustSize()
			
		elif(self.page == 0): 
			page = self.path + '000.jpg'
			self.strPage = page
			self.imageLabel.setPixmap(QtGui.QPixmap(page))
			self.imageLabel.adjustSize()
	
	def changes(self):
		self.window = teste.Ui_Dialog()
		self.window.name = self.strPage
		print(self.window.name)
		self.window.show()
	
	def zoomIn(self):
		self.scaleImage(1.25)
 
	def zoomOut(self):
		self.scaleImage(0.8)

	def normalSize(self):
		self.imageLabel.adjustSize()
		self.scaleFactor = 1.0
	
	def createActions(self):

		#Zoom
		self.zoomInAct = QtGui.QAction("Zoom &In (25%)", self, shortcut="Ctrl+=", enabled=False, triggered=self.zoomIn)
		self.zoomOutAct = QtGui.QAction("Zoom &Out (25%)", self,shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)
		self.normalSizeAct = QtGui.QAction("&Normal Size", self,shortcut="Ctrl+S", enabled=False, triggered=self.normalSize)
		self.fitToWindowAct = QtGui.QAction("&Fit to Window", self, enabled=False, checkable=True, shortcut="Ctrl+F", triggered=self.fitToWindow)

		#Pages
		self.NextPage = QtGui.QAction("Next", self,shortcut="right", enabled=False, triggered=self.nextPage)
		self.PreviusPage = QtGui.QAction("Previous", self,shortcut="left", enabled=False, triggered=self.previusPage)
		self.Changes = QtGui.QAction("Image Settings", self,shortcut="Ctrl+T", enabled=False, triggered=self.changes)
		 
		#About Mangax
		self.aboutAct = QtGui.QAction("&About", self, triggered=self.about)

		#Exit
		self.exitAct = QtGui.QAction("E&xit", self, shortcut="Ctrl+Q",triggered=self.close)


	def updateActions(self):
		self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
		self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
		self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())                

		#OLHAR MAIS TARDE
		self.NextPage.setEnabled(not self.exitAct.isChecked())
		self.PreviusPage.setEnabled(not self.exitAct.isChecked())
		self.Changes.setEnabled(not self.exitAct.isChecked())
		
	def scaleImage(self, factor):
		self.zoomInAct.setEnabled(self.scaleFactor < 3.0)


	def createMenus(self):

		#File Functions
		self.fileMenu = QtGui.QMenu("&File", self)
		#self.fileMenu.addAction(self.openAct)
		#self.fileMenu.addAction(self.printAct)
		#self.fileMenu.addSeparator()
		self.fileMenu.addAction(self.exitAct)

		#View Functions
		self.viewMenu = QtGui.QMenu("&View", self)
		self.viewMenu.addAction(self.zoomInAct)
		self.viewMenu.addAction(self.zoomOutAct)
		self.viewMenu.addAction(self.normalSizeAct)
		self.viewMenu.addSeparator()
		self.viewMenu.addAction(self.NextPage)
		self.viewMenu.addAction(self.PreviusPage)
		self.viewMenu.addSeparator()
		self.viewMenu.addAction(self.Changes)
		
		#About Mangax
		self.helpMenu = QtGui.QMenu("&Help", self)
		self.helpMenu.addAction(self.aboutAct)

		self.menuBar().addMenu(self.fileMenu)
		self.menuBar().addMenu(self.viewMenu)
		self.menuBar().addMenu(self.helpMenu)

	def scaleImage(self, factor):
		
		self.scaleFactor *= factor
		self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

		self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
		self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

		self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
		
	def adjustScrollBar(self, scrollBar, factor):
		scrollBar.setValue(int(factor * scrollBar.value()+ ((factor - 1) * scrollBar.pageStep()/2)))

	def about(self):
		QtGui.QMessageBox.about(self, "About Mangax",
        	"<p>The <b>Mangax</b>")
			
		

if __name__ == '__main__':
 
	import sys

	app = QtGui.QApplication(sys.argv)
	ex = Ui_Form()

#	p = ex.palette()
#	p.setColor(ex.backgroundRole(), QtCore.Qt.black)
#	ex.setPalette(p)
	ex.show()
#	ex.showFullScreen()
	sys.exit(app.exec_())

