#! /usr/bin/env env
# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui
import ExtendedQLabel
import teste
import os
import glob
import thumbnails

class Ui_Form(QtGui.QMainWindow):

	def __init__(self):
		self.path = os.getcwd() + '/c060/'
		print(self.path)
		self.manga = 'berserk'
		print(self.manga)
		self.page = 0
		self.scaleFactor = 1.0


		self.chapters = self._images()

		# Find the matching files for each valid
		# extension and add them to the images list
		# pattern = os.path.join(self.path,'*.jpg')
		# self.chapters.extend(glob.glob(pattern))
		# self.chapters.sort()

		super(Ui_Form, self).__init__()
		self.setupUi(self)
		

	def _images(self):
		# Start with an empty list
		images = []

		# Find the matching files for each valid
		# extension and add them to the images list
		pattern = os.path.join(self.path,'*.jpg')
		print glob.glob(pattern)
		images.extend(glob.glob(pattern))

		images.sort()
		return images
		
	def setupUi(self, Form):
		
		Form.setObjectName("Form")
		Form.resize(1366, 768)
		
		self.imageLabel = ExtendedQLabel.ExtendedQLabel(Form)
		self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
		self.imageLabel.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
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
		
		# creating commandLinkButtons
		self.commandLinkButton = QtGui.QCommandLinkButton(Form)
		self.commandLinkButton_2 = QtGui.QCommandLinkButton(Form)

		# creating lineEdit
		self.lineEdit = QtGui.QLineEdit(Form)
		self.lineEdit.setGeometry(QtCore.QRect(0, 0, 113, 27))

		# input's font
		font = QtGui.QFont()
		font.setFamily("Purisa")
		font.setWeight(75)
		font.setItalic(True)
		font.setBold(True)
		self.lineEdit.setFont(font)
		self.lineEdit.setFocusPolicy(QtCore.Qt.ClickFocus)

		# creating spinBox "chapters"
		self.spinBox = QtGui.QSpinBox(Form)
		self.spinBox.setGeometry(QtCore.QRect(0, 0, 113, 27))
		self.spinBox.setMinimum(0)
		self.spinBox.setMaximum(1000)
		QtCore.QObject.connect(self.spinBox, QtCore.SIGNAL('valueChanged(int)'), self.changeChapterSpinBox)

		# creating thumbnails
		self.win = QtGui.QWidget(Form)
		self.win.setGeometry(QtCore.QRect(0, 0, 1366, 768))
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHeightForWidth(self.win.sizePolicy().hasHeightForWidth())
		self.thumb = thumbnails.ImageFileList(self.path, self.win)
		self.thumb.setSizePolicy(sizePolicy)
		
		# creating spacer 
		self.spacer = QtGui.QSpacerItem(778, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)

		# Main window properties
		self.widget = QtGui.QWidget(Form)
		self.widget.setGeometry(QtCore.QRect(0, 0, 1366, 768))

		# creating layouts 
		self.verticalLayout = QtGui.QVBoxLayout(self.widget)
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)
		self.horizontalLayout = QtGui.QHBoxLayout()
		self.horizontalLayout_2 = QtGui.QHBoxLayout()
		self.verticalLayout_2 = QtGui.QVBoxLayout()
		
		# horizontalLayout <- commandLinkButtons and lineEdit
		self.horizontalLayout.addWidget(self.commandLinkButton)
		self.horizontalLayout.addWidget(self.commandLinkButton_2)
		self.horizontalLayout.addItem(self.spacer)
		self.horizontalLayout.addWidget(self.lineEdit)
		self.horizontalLayout.addWidget(self.spinBox)

		# verticalLayout <- horizontalLayout
		self.verticalLayout.addLayout(self.horizontalLayout)


		# horizontalLayout <- thumbnails
		self.horizontalLayout_2.addWidget(self.thumb)
		self.horizontalLayout_2.addWidget(self.scrollArea)

		# verticalLayout <- scrollArea
		#self.verticalLayout_2.addWidget(self.scrollArea)

		self.verticalLayout.addLayout(self.horizontalLayout_2)
 
		self.createActions()
		self.createMenus()
		
		self.updateActions()

		self.retranslateUi(Form)

		QtCore.QMetaObject.connectSlotsByName(Form)

	def retranslateUi(self, Form):
		Form.setWindowTitle(QtGui.QApplication.translate("Form", "Mangax", None, QtGui.QApplication.UnicodeUTF8))
		self.lineEdit.setPlaceholderText(QtGui.QApplication.translate("Form", "Mangá Title", None, QtGui.QApplication.UnicodeUTF8))
		self.lineEdit.setToolTip(QtGui.QApplication.translate("Form", "Title", None, QtGui.QApplication.UnicodeUTF8))
		self.spinBox.setToolTip(QtGui.QApplication.translate("Form", "Chapters", None, QtGui.QApplication.UnicodeUTF8))


	

		print(self.chapters[self.page])
		self.imageLabel.setPixmap(QtGui.QPixmap(self.chapters[self.page]))
		self.imageLabel.adjustSize()
		
		# scale image
		self.scaleImage(0.8)
		self.scaleImage(0.8)

		self.setSpinBoxMaximum()

	def setSpinBoxMaximum(self):
		# set Max spinBox		
		self.spinBox.setMaximum(len(self.chapters)-1)

	def resetScroll(self):
		# reset verticalscrollbar's position when the page is changed
		self.scrollArea.verticalScrollBar().setValue(0)
		# reset horizontalscrollbar's position when the page is changed
		self.scrollArea.horizontalScrollBar().setValue(0)
		# handling zoom
		self.scaleFactor = 1.0

	# Verificar
	def changeChapterSpinBox(self,value):
		if(self.flagChangeSpinBox):
			self.resetScroll()

			self.imageLabel.setPixmap(QtGui.QPixmap(self.chapters[value]))
			self.imageLabel.adjustSize()

			# scale image
			self.scaleImage(0.8)
			self.scaleImage(0.8)

		self.page = value
		self.flagChangeSpinBox = True


	def fitToWindow(self):
		fitToWindow = self.fitToWindowAct.isChecked()
		self.scrollArea.setWidgetResizable(fitToWindow)
		if not fitToWindow:
			self.normalSize()
		self.updateActions()
	
	def nextPage(self):

		self.resetScroll()

		if(self.page <= len(self.chapters)):
			# handling pages
			self.page += 1
			self.flagChangeSpinBox = False
			self.spinBox.setProperty("value", self.page)
			#self.flagChangeSpinBox = True
			print self.page

			if(self.page == len(self.chapters)):
				self.page -= 1
				msgBox = QtGui.QMessageBox()
				msgBox.setWindowTitle("End")
				msgBox.setText("End of Chapter.")
				msgBox.exec_()
			else:
				print (self.chapters[self.page])
				self.imageLabel.setPixmap(QtGui.QPixmap(self.chapters[self.page]))
				self.imageLabel.adjustSize()

			#scale image
			self.scaleImage(0.8)
			self.scaleImage(0.8)
		
	def previusPage(self):

		self.resetScroll()
		
		if(self.page != 0):
			self.page -= 1
			self.flagChangeSpinBox = False
			self.spinBox.setProperty("value", self.page)
			#self.flagChangeSpinBox = True

			print self.page
			print (self.chapters[self.page])
			self.imageLabel.setPixmap(QtGui.QPixmap(self.chapters[self.page]))
			self.imageLabel.adjustSize()
			
		elif(self.page == 0): 
			print (self.chapters[self.page])
			self.imageLabel.setPixmap(QtGui.QPixmap(self.chapters[self.page]))
			self.imageLabel.adjustSize()

		#scale image
		self.scaleImage(0.8)
		self.scaleImage(0.8)

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
		
	#def scaleImage(self, factor):
	#	self.zoomInAct.setEnabled(self.scaleFactor < 3.0)


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
		self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)
		
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

