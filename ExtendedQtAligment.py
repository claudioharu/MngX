from PySide import QtCore, QtGui
 
class ExtendedQLabel(QtCore.Qt):
 
    def __init(self, parent):
		QtGui.Qt.__init__(self, parent)
 
    def mouseReleaseEvent(self, ev):
        self.emit(QtCore.SIGNAL('clicked()'))
