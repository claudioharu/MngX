#! /usr/bin/env env
# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui
import ExtendedQLabel
import teste
import os
import glob
import thumbnails
from foxy import *
from Thread import *

class Ui_Form(QtGui.QMainWindow):

	def __init__(self):

			
		self.path = os.getcwd() + '/c060/'
		print(self.path)
		self.manga = 'tenkuu_shinpan'
		print(self.manga)
		self.page = 0
		self.pathIndex = 0
		self.scaleFactor = 1.0
		self.lightOn = False
		self.increasePressed = True
		self.decreasePressed = False
		self.paths = self._paths()
		self.flagChangeSpinBox = True

		# self.spider = QtGui.QWidget()

		self.updatePath()
		self.chapters = self._images()

		# Find the matching files for each valid
		# extension and add them to the images list
		# pattern = os.path.join(self.path,'*.jpg')
		# self.chapters.extend(glob.glob(pattern))
		# self.chapters.sort()

		super(Ui_Form, self).__init__()

		self.setupUi(self)

	def updatePath(self):

		if self.paths:
			#verificar se paths estah vazio
			self.path = self.paths[self.pathIndex]

	def nextChapter(self):
		print "next"
		if self.paths:
			if self.pathIndex < len(self.paths): 
				self.pathIndex += 1
				print "Chapter" + str(self.pathIndex)
				self.path = self.paths[self.pathIndex]
				self.spinBox_2.setValue(self.pathIndex)
				

	def previousChapter(self):
		print "previous"
		if self.paths:
			print self.pathIndex
			if self.pathIndex > 0:
				self.pathIndex -= 1
				print "Chapter" + str(self.pathIndex)
				self.path = self.paths[self.pathIndex]
				
	def _paths(self):
		path = os.getcwd() + "/" + self.manga + "/"
		roots = []
		for root, dirs, files in os.walk(path):
			roots.append(root)

		roots = roots[1:]
		roots.sort()

		for root in roots:
			print root

		return roots
		
	def _images(self):
		# Start with an empty list
		images = []

		# Find the matching files for each valid
		# extension and add them to the images list
		pattern = os.path.join(self.path,'*.jpg')
		#print glob.glob(pattern)
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

		#image clicked()
		self.connect(self.imageLabel, QtCore.SIGNAL('clicked()'), self.nextPage)

		# pages Label
		self.label = QtGui.QLabel(Form)

		# chapters Label
		self.label_2 = QtGui.QLabel(Form)

		self.scrollArea = QtGui.QScrollArea()
		
		# collor white
		palette = QtGui.QPalette()
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
		self.scrollArea.setPalette(palette)
		
		# creating scrollArea
		self.scrollArea.setGeometry(QtCore.QRect(560, 70, 201, 571))
		self.scrollArea.setWidget(self.imageLabel)
		self.scrollArea.setAlignment(QtCore.Qt.AlignCenter)
		self.setCentralWidget(self.scrollArea)

		# creating icons
		lamp = QtGui.QIcon()
		lamp.addPixmap(QtGui.QPixmap("icons/lamp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		next = QtGui.QIcon()
		next.addPixmap(QtGui.QPixmap("icons/next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		previous = QtGui.QIcon()
		previous.addPixmap(QtGui.QPixmap("icons/previous.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		enlarge = QtGui.QIcon()
		enlarge.addPixmap(QtGui.QPixmap("icons/enlarge.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		resize = QtGui.QIcon()
		resize.addPixmap(QtGui.QPixmap("icons/resize.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		zOut = QtGui.QIcon()
		zOut.addPixmap(QtGui.QPixmap("icons/zoom_out.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		zIn = QtGui.QIcon()
		zIn.addPixmap(QtGui.QPixmap("icons/zoom_in.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		sch = QtGui.QIcon()
		sch.addPixmap(QtGui.QPixmap("icons/Search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

		# Lamp button
		self.toolButton = QtGui.QToolButton(Form) 
		self.toolButton.setAutoRaise(True)
		self.toolButton.setIcon(lamp)
		self.toolButton.setIconSize(QtCore.QSize(30, 30))
		QtCore.QObject.connect(self.toolButton, QtCore.SIGNAL("clicked()"), self.turnOff)

		# Next Button
		self.toolButton_2 = QtGui.QToolButton(Form)
		self.toolButton_2.setAutoRaise(True)
		self.toolButton_2.setIcon(next)
		self.toolButton_2.setIconSize(QtCore.QSize(30,30))
		QtCore.QObject.connect(self.toolButton_2, QtCore.SIGNAL("clicked()"), self.nextPage)

		# Previous Button
		self.toolButton_3 = QtGui.QToolButton(Form)
		self.toolButton_3.setAutoRaise(True)
		self.toolButton_3.setIcon(previous)
		self.toolButton_3.setIconSize(QtCore.QSize(30,30))
		QtCore.QObject.connect(self.toolButton_3, QtCore.SIGNAL("clicked()"), self.previousPage)

		# Enlarge Button
		self.toolButton_4 = QtGui.QToolButton(Form)
		self.toolButton_4.setAutoRaise(True)
		self.toolButton_4.setIcon(enlarge)
		self.toolButton_4.setIconSize(QtCore.QSize(30,30))
		QtCore.QObject.connect(self.toolButton_4, QtCore.SIGNAL("clicked()"), self.increase)

		# Resize Button
		self.toolButton_5 = QtGui.QToolButton(Form)
		self.toolButton_5.setAutoRaise(True)
		self.toolButton_5.setIcon(resize)
		self.toolButton_5.setIconSize(QtCore.QSize(30,30))
		QtCore.QObject.connect(self.toolButton_5, QtCore.SIGNAL("clicked()"), self.decrease)

		# Zoom In Button
		self.toolButton_6 = QtGui.QToolButton(Form)
		self.toolButton_6.setAutoRaise(True)
		self.toolButton_6.setIcon(zIn)
		self.toolButton_6.setIconSize(QtCore.QSize(40,40))	
		QtCore.QObject.connect(self.toolButton_6, QtCore.SIGNAL("clicked()"), self.zoomIn)	

		# Zoom Out Button
		self.toolButton_7 = QtGui.QToolButton(Form)
		self.toolButton_7.setAutoRaise(True)
		self.toolButton_7.setIcon(zOut)
		self.toolButton_7.setIconSize(QtCore.QSize(40,40))		
		QtCore.QObject.connect(self.toolButton_7, QtCore.SIGNAL("clicked()"), self.zoomOut)

		# Search Button
		self.toolButton_8 = QtGui.QToolButton(Form)
		self.toolButton_8.setAutoRaise(True)
		self.toolButton_8.setIcon(sch)
		self.toolButton_8.setIconSize(QtCore.QSize(28,28))
		QtCore.QObject.connect(self.toolButton_8, QtCore.SIGNAL("clicked()"), self.download)

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
		QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL('textChanged(QString)'), self.getManga)

		# creating spinBox "pages"
		self.spinBox = QtGui.QSpinBox(Form)
		self.spinBox.setGeometry(QtCore.QRect(0, 0, 113, 27))
		self.spinBox.setMinimum(0)
		self.spinBox.setMaximum(1000)
		QtCore.QObject.connect(self.spinBox, QtCore.SIGNAL('valueChanged(int)'), self.changePageSpinBox)

		# creating spinBox "chapters"
		self.spinBox_2 = QtGui.QSpinBox(Form)
		self.spinBox_2.setGeometry(QtCore.QRect(0, 0, 113, 27))
		self.spinBox_2.setMinimum(0)
		self.spinBox_2.setMaximum(1000)
		QtCore.QObject.connect(self.spinBox_2, QtCore.SIGNAL('valueChanged(int)'), self.changeChapterSpinBox)

		# creating thumbnails
		self.win = QtGui.QWidget(Form)
		self.win.setGeometry(QtCore.QRect(0, 0, 1366, 768))
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHeightForWidth(self.win.sizePolicy().hasHeightForWidth())
		self.thumb = thumbnails.ImageFileList(self.path, self.win)
		self.thumb.currentItemChanged.connect(self.itemChanged)
		self.thumb.setMaximumWidth(self.thumb.sizeHintForColumn(0)+20)
		self.thumb.setSizePolicy(sizePolicy)

		# creating spacer 
		self.spacer = QtGui.QSpacerItem(508, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.spacer2 = QtGui.QSpacerItem(10, 0, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
		
		# Main window properties
		self.widget = QtGui.QWidget(Form)
		self.widget.setGeometry(QtCore.QRect(0, 0, 1366, 748))

		# creating layouts
		self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
		self.horizontalLayout.setContentsMargins(0,0,0,0)

		self.horizontalLayout.addWidget(self.thumb)

		self.verticalLayout = QtGui.QVBoxLayout()

		self.horizontalLayout_2 = QtGui.QHBoxLayout()
		self.horizontalLayout_2.addWidget(self.toolButton_4)
		self.horizontalLayout_2.addWidget(self.toolButton_5)
		self.horizontalLayout_2.addWidget(self.toolButton_6)
		self.horizontalLayout_2.addWidget(self.toolButton_7)
		self.horizontalLayout_2.addWidget(self.toolButton)
		self.horizontalLayout_2.addItem(self.spacer)
		self.horizontalLayout_2.addWidget(self.label_2)
		self.horizontalLayout_2.addWidget(self.spinBox_2)
		self.horizontalLayout_2.addWidget(self.label)
		self.horizontalLayout_2.addWidget(self.spinBox)
		self.horizontalLayout_2.addWidget(self.lineEdit)
		self.horizontalLayout_2.addWidget(self.toolButton_8)
		

		self.progressBar = QtGui.QProgressBar(Form)
		self.progressBar.setProperty("value", 1)
		
		self.horizontalLayout_2.addWidget(self.progressBar)

		self.verticalLayout.addLayout(self.horizontalLayout_2)
		self.horizontalLayout_3 = QtGui.QHBoxLayout()
		self.horizontalLayout_3.addWidget(self.toolButton_3)
		self.horizontalLayout_3.addWidget(self.scrollArea)
		self.horizontalLayout_3.addWidget(self.toolButton_2)

		self.verticalLayout.addLayout(self.horizontalLayout_3)

		self.horizontalLayout.addLayout(self.verticalLayout)

		self.createActions()
		self.createMenus()
		
		self.updateActions()

		self.retranslateUi(Form)
		self.setWindowIcon(QtGui.QIcon("icons/mangaYouIcon.png"))
		QtCore.QMetaObject.connectSlotsByName(Form)

	def retranslateUi(self, Form):
		Form.setWindowTitle(QtGui.QApplication.translate("Form", "MangaYou", None, QtGui.QApplication.UnicodeUTF8))
		self.lineEdit.setPlaceholderText(QtGui.QApplication.translate("Form", "  Mangá Title", None, QtGui.QApplication.UnicodeUTF8))
		self.lineEdit.setToolTip(QtGui.QApplication.translate("Form", "Title", None, QtGui.QApplication.UnicodeUTF8))
		self.spinBox.setToolTip(QtGui.QApplication.translate("Form", "Pages", None, QtGui.QApplication.UnicodeUTF8))
		self.label.setText(QtGui.QApplication.translate("Form", "Pages:", None, QtGui.QApplication.UnicodeUTF8))
		self.label_2.setText(QtGui.QApplication.translate("Form", "Chapters:", None, QtGui.QApplication.UnicodeUTF8))
		self.toolButton_8.setToolTip(QtGui.QApplication.translate("Form", "Search", None, QtGui.QApplication.UnicodeUTF8))

		print(self.chapters[self.page])
		self.imageLabel.setPixmap(QtGui.QPixmap(self.chapters[self.page]))
		self.imageLabel.adjustSize()
		self.thumb.item(self.page).setSelected(True)

		# scale image
		self.scaleImage(0.8)
		self.scaleImage(0.8)

		self.setSpinBoxMaximum()
		if(len(self.paths) > 0):
			self.spinBox_2.setMaximum(len(self.paths)-1)


	# Get manga's name
	def getManga(self, title):
		print self.manga
		if(title != ""):
			self.manga = title
			print self.manga

	# Start the download
	def download(self):
		# Treating titles
		title = self.manga.split(" ")
		self.manga = ""
		for t in title:
			self.manga += str(t) + "_"

		self.manga = self.manga[:-1]
		print "Downloading " + self.manga

		title = self.manga
		self.lineEdit.clear()
		self.imageLabel.setFocus()

		import Thread
		self.thread = Thread.Thread()
		self.thread.notifyProgress.connect(self.setProgress)
		self.thread.setTitle(title)
		self.thread.start()

		# newpid = os.fork()
		# pid = os.getpid()
		# if newpid == 0:
		# 	print "filho"
		# 	import sys
		
		# 	# os.system("python qpaint.py")
		# 	os.system("python foxy.py " + str(title))
		# 	os._exit(0)  


		# self.spinBox_2.setMaximum(len(self.paths)-1)

	def setProgress(self, progress):
		self.progressBar.setValue(progress)
		print "Progress value: " + str(progress)

		if(progress == 100):
			self.paths = self._paths()
			self.pathIndex = 0
			self.updatePath()
			self.chapters = self._images()
			self.page = 0

			self.imageLabel.setPixmap(QtGui.QPixmap(self.chapters[self.page]))
			self.imageLabel.adjustSize()
			self.thumb.item(self.page).setSelected(True)

			# scale image
			self.scaleImage(0.8)
			self.scaleImage(0.8)




	def increase(self):
		# print "increase"
		if(self.increasePressed):
			b = self.horizontalLayout.takeAt(0)
			w = b.widget()
			w.setParent(None)	
			del b

			self.increasePressed = False
			self.decreasePressed = True
			self.showFullScreen()


	def decrease(self):
		# print "decrease"
		if(self.decreasePressed):
			b = self.horizontalLayout.takeAt(0)
			w = b.layout()
			w.setParent(None)
			del b
			
			self.decreasePressed = False
			self.increasePressed = True
			self.horizontalLayout.addWidget(self.thumb)
			self.horizontalLayout.addLayout(self.verticalLayout)
			self.showMaximized() 	
			self.thumb._scroll(self.page)
		# else:
		# 	print "i cant decrease"

	def itemChanged(self, curr, prev):
		# print self.thumb.currentRow()

		self.page = self.thumb.currentRow()

		self.resetScroll()
		self.imageLabel.setPixmap(QtGui.QPixmap(self.chapters[self.page]))
		self.imageLabel.adjustSize()

		self.flagChangeSpinBox = False
		self.spinBox.setProperty("value", self.page)

		# scale image
		self.scaleImage(0.8)
		self.scaleImage(0.8)

	# Turn off the light
	def turnOff(self):
		
		palette = QtGui.QPalette()
		if(not self.lightOn):
			# print "on"
			brush = QtGui.QBrush(QtGui.QColor(24, 24, 24))
			brush.setStyle(QtCore.Qt.SolidPattern)
			palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
			self.lightOn = True
		else:
			# print "off"
			brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
			brush.setStyle(QtCore.Qt.SolidPattern)
			palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
			self.lightOn = False
			
		self.scrollArea.setPalette(palette)
	
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


	def changeChapterSpinBox(self, value):
		print value
		self.pathIndex = value
		print "Chapter" + str(self.pathIndex)
		self.path = self.paths[self.pathIndex]

		self.thumb._update(self.path)
		self.chapters = self._images()
			
		if(self.page == 0):
			self.changePageSpinBox(self.page)
		else:
			self.page = 0
			self.spinBox.setProperty("value", self.page)

	# Verificar
	def changePageSpinBox(self,value):
		if(self.flagChangeSpinBox):
			self.resetScroll()
			self.thumb.item(value).setSelected(True)
			self.thumb._scroll(value)
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
				
				# SE TIVER MAIS CAPITULOS
				# TEM QUE VERIFICAR
				self.page = 0
				self.spinBox.setValue(0)
				
				self.nextChapter()
				self.chapters = self._images()

				# Treating thumbnails
				self.thumb._update(self.path)
				self.thumb._scroll(self.page)
				self.thumb.item(self.page).setSelected(True)

 				self.resetScroll()

				self.imageLabel.setPixmap(QtGui.QPixmap(self.chapters[self.page]))
				self.imageLabel.adjustSize()

			else:
				print (self.chapters[self.page])
				self.thumb.item(self.page).setSelected(True)
				self.thumb._scroll(self.page)
				self.imageLabel.setPixmap(QtGui.QPixmap(self.chapters[self.page]))
				self.imageLabel.adjustSize()

			#scale image
			self.scaleImage(0.8)
			self.scaleImage(0.8)
		
	def previousPage(self):
		
		self.resetScroll()
		
		if(self.page > 0):
			self.page -= 1
			self.flagChangeSpinBox = False
			self.spinBox.setProperty("value", self.page)
			#self.flagChangeSpinBox = True

			# print self.page
			# print (self.chapters[self.page])
			# Treating thumbnails
			self.thumb.item(self.page).setSelected(True)
			self.thumb._scroll(self.page)

			self.imageLabel.setPixmap(QtGui.QPixmap(self.chapters[self.page]))
			self.imageLabel.adjustSize()
			
		else:
			self.previousChapter()
			self.chapters = self._images()
			self.resetScroll()
			
			# Treating thumbnails
			self.thumb._update(self.path)
			self.thumb.item(self.page).setSelected(True)
			self.thumb._scroll(self.page)

			self.imageLabel.setPixmap(QtGui.QPixmap(self.chapters[self.page]))
			self.imageLabel.adjustSize()
			# print (self.chapters[self.page])
			# self.imageLabel.setPixmap(QtGui.QPixmap(self.chapters[self.page]))
			# self.imageLabel.adjustSize()

		#scale image
		self.scaleImage(0.8)
		self.scaleImage(0.8)
	
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
		self.lightInAct = QtGui.QAction("Lights", self, shortcut="Esc", enabled=False, triggered=self.turnOff)
		
		#Pages
		self.NextPage = QtGui.QAction("Next", self,shortcut="right", enabled=False, triggered=self.nextPage)
		self.PreviousPage = QtGui.QAction("Previous", self,shortcut="left", enabled=False, triggered=self.previousPage)
		# self.Changes = QtGui.QAction("Image Settings", self,shortcut="Ctrl+T", enabled=False, triggered=self.changes)
		
		# Paint
		self.paintAct = QtGui.QAction("Paint", self, triggered=self.Paint)

		#About MangaYou
		self.aboutAct = QtGui.QAction("&About", self, triggered=self.about)

		#Exit
		self.exitAct = QtGui.QAction("E&xit", self, shortcut="Ctrl+Q",triggered=self.close)


	def updateActions(self):
		self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
		self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
		self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())                

		#OLHAR MAIS TARDE
		self.NextPage.setEnabled(not self.exitAct.isChecked())
		self.PreviousPage.setEnabled(not self.exitAct.isChecked())
		self.lightInAct.setEnabled(not self.exitAct.isChecked())

	def createMenus(self):

		#File Functions
		self.fileMenu = QtGui.QMenu("&File", self)
		self.fileMenu.addAction(self.exitAct)

		#View Functions
		self.viewMenu = QtGui.QMenu("&View", self)
		self.viewMenu.addAction(self.zoomInAct)
		self.viewMenu.addAction(self.zoomOutAct)
		self.viewMenu.addAction(self.normalSizeAct)
		self.viewMenu.addSeparator()
		self.viewMenu.addAction(self.NextPage)
		self.viewMenu.addAction(self.PreviousPage)
		self.viewMenu.addAction(self.lightInAct)
		self.viewMenu.addSeparator()
		self.viewMenu.addAction(self.paintAct)
		
		#About MangaYou
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
		QtGui.QMessageBox.about(self, "About MangaYou",
        	"<p>The <b>MangaYou</b>")
			
	def Paint(self):
		import myPaint
		m = myPaint.MainWindow()
		m.show()
		

if __name__ == '__main__':
 
	import sys
	app = QtGui.QApplication(sys.argv)
	ex = Ui_Form()

	ex.showMaximized()

	sys.exit(app.exec_())

