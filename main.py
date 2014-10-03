from PySide import QtCore, QtGui

class Ui_MainWindow(object):

      def setupUi(self, MainWindow, AppObj):

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionProcess = QtGui.QAction(MainWindow)
        self.actionProcess.setObjectName("actionProcess")
        # self.actionProcess.triggered.connect(self.myappObj.menuActionProcess) 

    