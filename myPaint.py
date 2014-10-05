#!/usr/bin/env python

# These are only needed for Python v2 but are harmless for Python v3.
import sys
#import sip
#sip.setapi('QString', 2)
#sip.setapi('QVariant', 2)

from PySide import QtCore, QtGui
from paint import paintArea


class MainWindow(QtGui.QMainWindow):

    def __init__(self):
    
        super(MainWindow, self).__init__()

        self.saveAsActs = []

        self.paintArea = paintArea(self)
        self.paintArea.clearImage()
        self.paintArea.clearImagePreview()
        self.paintArea.mainWindow = self
        self.setCentralWidget(self.paintArea)

        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)        

        self.createActions()

        self.saveAsMenu = QtGui.QMenu("&Save As", self)
        for action in self.saveAsActs:
            self.saveAsMenu.addAction(action)

        fileMenu = QtGui.QMenu("&File", self)
        fileMenu.addAction(self.openImage)
        fileMenu.addMenu(self.saveAsMenu)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAct)

        editMenu = QtGui.QMenu("&Edit", self)
        editMenu.addAction(self.penColorAct)
        editMenu.addAction(self.penWidthAct)
        editMenu.addSeparator()
        editMenu.addAction(self.clearScreenAct)

        helpMenu = QtGui.QMenu("&Help", self)
        helpMenu.addAction(self.aboutAct)

        self.menuBar().addMenu(fileMenu)
        self.menuBar().addMenu(editMenu)
        self.menuBar().addMenu(helpMenu)
        
        #toolbar and actions:
        self.toolbar = self.addToolBar('toolbar')
        self.toolbar.addAction(self.pen)
        self.toolbar.addAction(self.line)
        self.toolbar.addAction(self.PenWidth)
        self.toolbar.addAction(self.PenColor)
        self.toolbar.addAction(self.eraser)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.zoomIn)
        self.toolbar.addAction(self.zoomOut)        
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.mirror_w)
        self.toolbar.addAction(self.mirror_h)


        self.setWindowTitle("Paint")
        # self.setWindowIcon(QtGui.QIcon("icon/paint.png"))
        self.setGeometry(300, 100, 600, 600)
        self.resize(self.paintArea.sizew, self.paintArea.sizeh+85)
        self.statusBar()

    def open(self):
        if self.maybeSave():
            fileName = QtGui.QFileDialog.getOpenFileName(self, "Open File",
                QtCore.QDir.currentPath())
            if fileName:
                self.paintArea.openImage(fileName)
        

    def zoomIn(self):
        self.paintArea.zoomIn()

    def zoomOut(self):
        self.paintArea.zoomOut()

    def setPen(self):
        self.paintArea.setTool('pen')
        
    def setLine(self):
        self.paintArea.setTool('line')

    def setEraser(self):
        self.paintArea.setTool('eraser')
        
    def setMirror_w(self):
        self.paintArea.mirror_w()
        
    def setMirror_h(self):
        self.paintArea.mirror_h()

    def createActions(self):
    
        self.openImage = QtGui.QAction("&Open...", self, icon=QtGui.QIcon('icon/open.png'), shortcut="Ctrl+O", triggered=self.open)

        for format in QtGui.QImageWriter.supportedImageFormats():
            format = str(format)
            text = format.upper() + "..."
            action = QtGui.QAction(text, self, triggered=self.save)
            action.setData(format)
            self.saveAsActs.append(action)

        #menu actions:
        self.exitAct = QtGui.QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        self.penColorAct = QtGui.QAction("&Pen Color...", self, icon=QtGui.QIcon('icons/pencolor.png'),triggered=self.penColor)
        self.penWidthAct = QtGui.QAction("Pen &Width...", self, icon=QtGui.QIcon('icons/pensize.png'), triggered=self.penWidth)
        self.clearScreenAct = QtGui.QAction("&Clear Screen", self, icon=QtGui.QIcon('icons/clear.png'), shortcut="Ctrl+L", triggered=self.paintArea.clearImage)
        self.aboutAct = QtGui.QAction("&About", self, shortcut="F1", triggered=self.about)
        self.aboutAct.setStatusTip('About program')

        self.pen = QtGui.QAction("", self, icon=QtGui.QIcon('icons/pen.png'), triggered=self.setPen)
        self.pen.setStatusTip('using pen')
        
        self.line = QtGui.QAction("", self, icon=QtGui.QIcon('icons/line.png'), triggered=self.setLine)
        self.PenWidth = QtGui.QAction("", self, icon=QtGui.QIcon('icons/pensize.png'), triggered=self.penWidth)
        self.PenColor = QtGui.QAction("", self, icon=QtGui.QIcon('icons/pencolor.png'), triggered=self.penColor)
        self.zoomIn = QtGui.QAction("", self, icon=QtGui.QIcon('icons/zoom_in.png'), triggered=self.zoomIn)
        self.zoomOut = QtGui.QAction("", self, icon=QtGui.QIcon('icons/zoom_out.png'), triggered=self.zoomOut)
        self.eraser = QtGui.QAction("", self, icon=QtGui.QIcon('icons/erase.png'), triggered=self.setEraser)
        self.mirror_w = QtGui.QAction("", self, icon=QtGui.QIcon('icons/mirror-w.png'), triggered=self.setMirror_w)
        self.mirror_h = QtGui.QAction("", self, icon=QtGui.QIcon('icons/mirror-h.png'), triggered=self.setMirror_h)

    def save(self):
        action = self.sender()
        fileFormat = action.data()
        print fileFormat
        self.saveFile(fileFormat)


    def penColor(self):
        newColor = QtGui.QColorDialog.getColor(self.paintArea.penColor())
        if newColor.isValid():
            self.paintArea.setPenColor(newColor)


    def penWidth(self):
        newWidth, ok = QtGui.QInputDialog.getInteger(self, "paint",
            "Select pen width:", self.paintArea.penWidth(), 1, 50, 1)
        if ok:
            self.paintArea.setPenWidth(newWidth)


    def about(self):
        QtGui.QMessageBox.about(self, "Paint", 
            "<p> Inspired by Mohammad Honarmand(jhm)</p>"
            )

    def maybeSave(self):
        if self.paintArea.isModified():
            ret = QtGui.QMessageBox.warning(self, "QPaint",
                "The image has been modified.\n"
                "Do you want to save your changes?",
                QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard |
                QtGui.QMessageBox.Cancel)
            if ret == QtGui.QMessageBox.Save:
                return self.saveFile('png')
            elif ret == QtGui.QMessageBox.Cancel:
                return False

        return True

    def saveFile(self, fileFormat):
        initialPath = QtCore.QDir.currentPath() + '/untitled.' + fileFormat

        fileName = QtGui.QFileDialog.getSaveFileName(self, "Save As",
            initialPath,
            "%s Files (*.%s);;All Files (*)" % (fileFormat.upper(), fileFormat))
        if fileName:
            return self.paintArea.saveImage(fileName, fileFormat)

        return False
                
def main():
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    ex.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
