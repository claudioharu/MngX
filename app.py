from PySide import QtCore, QtGui
from main import Ui_MainWindow

class App(QtGui.QDialog):
      def __init__(self, parent=None):
          self.__mainWindow = QtGui.QMainWindow()
          self.__mainWindowDesignContext = Ui_MainWindow()
          self.__mainWindowDesignContext.setupUi(self.__mainWindow, self)
          self.__mainWindow.show()
      def menuActionProcess(self):
          self.processThread = BatchProcesser()
          self.progressBar = QtGui.QProgressBar()
          statusBar.addWidget(self.progressBar)
          self.progressBar.show()
          self.progressBar.setMinimum(0)
          self.progressBar.setMaximum(100)
          QtCore.QObject.connect(self.processThread, QtCore.SIGNAL("progress(int)"),self.progressBar, QtCore.SLOT("setValue(int)"), QtCore.Qt.QueuedConnection)
          if not self.processThread.isRunning():
              self.processThread.exiting = False
              self.processThread.start()

import sys

app = QtGui.QApplication(sys.argv)
ex = App()

# p = ex.palette()
# p.setColor(ex.backgroundRole(), QtCore.Qt.black)
# ex.setPalette(p)
ex.show()
# ex.showFullScreen()
sys.exit(app.exec_())       