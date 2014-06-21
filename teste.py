# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'teste.ui'
#
# Created: Sun May 25 12:13:57 2014
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
import sys
#import manga

class Ui_Dialog(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.contrast = 0
        self.brightness = 1.0
		

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(228, 172)
        self.widget = QtGui.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(0, 0, 227, 171))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lineEdit = QtGui.QLineEdit(self.widget)
        self.lineEdit.setInputMask("")
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_3.addWidget(self.lineEdit)
        self.buttonBox = QtGui.QDialogButtonBox(self.widget)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_3.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.horizontalSlider = QtGui.QSlider(self.widget)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalLayout.addWidget(self.horizontalSlider)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.bright = QtGui.QDoubleSpinBox(self.widget)
        self.bright.setMinimum(1.0)
        self.bright.setMaximum(3.0)
        self.bright.setObjectName("bright")
        self.verticalLayout.addWidget(self.bright)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.retranslateUi(Dialog)
        
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        QtCore.QObject.connect(self.horizontalSlider, QtCore.SIGNAL('valueChanged(int)'), self.getContrastValue)
        QtCore.QObject.connect(self.bright, QtCore.SIGNAL('valueChanged(double)'), self.getBrightnessValue)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.setContrast)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.cancel)
        QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL("textChanged(QString)"), self.getManga)
		    
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit.setPlaceholderText(QtGui.QApplication.translate("Dialog", "Insira o mangá", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "100", None, QtGui.QApplication.UnicodeUTF8))
		
    def getContrastValue(self, value):
        self.contrast = value
        print(self.contrast)
    
    def getBrightnessValue(self, value):
		self.brightness = value
		print(self.brightness)

    def setContrast(self):
        manga.sharp(self.name)
        manga.contrast(self.name)
        #manga.dinamicContrast(1.0, self.brightness, self.name)
        return QtGui.QWidget.close(self)

    def cancel(self):
        return QtGui.QWidget.close(self)
       
    def getManga(self, name):
		self.name = name
		print(self.name)

# if __name__ == '__main__':
#        app = QtGui.QApplication(sys.argv)
#        ex = Ui_Dialog()
#        ex.show()
#        sys.exit(app.exec_())
