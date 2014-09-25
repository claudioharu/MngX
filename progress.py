from PySide import QtCore, QtGui

class Progress(QtGui.QWidget):


    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.resize(400, 300)
        self.progressBar = QtGui.QProgressBar(self)
        self.progressBar.setGeometry(QtCore.QRect(60, 50, 118, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.spinBox = QtGui.QSpinBox(self)
        self.spinBox.setGeometry(QtCore.QRect(50, 170, 60, 27))
        self.spinBox.setObjectName("spinBox")

        self.retranslateUi(self)
        QtCore.QObject.connect(self.spinBox, QtCore.SIGNAL("valueChanged(int)"), self.progressBar.setValue)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))

# if __name__ == '__main__':
 
#     import sys

#     app = QtGui.QApplication(sys.argv)
#     ex = Progress()

# #   p = ex.palette()
# #   p.setColor(ex.backgroundRole(), QtCore.Qt.black)
# #   ex.setPalette(p)
#     ex.show()
# #   ex.showFullScreen()
#     sys.exit(app.exec_())
