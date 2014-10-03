from PySide.QtGui import *
from PySide.QtCore import *

class BatchProcesser(QThread):
     __errorHappened = False
     def __init__(self, parent=None):
         QThread.__init__(self, parent)
         self.exiting = False
     def run(self):
         for a in range(101):
            print a
            QThread.msleep(100)
            self.emit(SIGNAL("progress(int)"), a)
            print a