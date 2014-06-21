from PySide import QtCore, QtGui
 
class ExtendedQLabel(QtGui.QLabel):
 
    def __init(self, parent):
		QtGui.QLabel.__init__(self, parent)
 
    def mouseReleaseEvent(self, ev):
        self.emit(QtCore.SIGNAL('clicked()'))
