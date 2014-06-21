#! /usr/bin/env env

import sys
from PySide import QtCore, QtGui, QtWebKit


app = QtGui.QApplication(sys.argv)
b = QtWebKit.QWebView()

QtWebKit.QWebSettings.globalSettings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled,True)
b.load(QtCore.QUrl('http://grooveshark.com/#!/search?q=elvenking'))
b.show()
app.exec_()

