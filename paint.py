from PySide import QtCore, QtGui

class paintArea(QtGui.QWidget):
       
    tools = { 'pen':True,
        'line':False,
        'temp':False,
        'flag':False,
        'eraser':False,
        }

    def __init__(self, parent=None):
        super(paintArea, self).__init__(parent)

        self.autoFillBackground = True
        self.pWidth = 4
        self.pColor = QtGui.QColor(100, 100, 100, 255)
        imageSize = QtCore.QSize(800, 500)
        self.image = QtGui.QImage(imageSize, QtGui.QImage.Format_RGB32)
        self.tempImage = QtGui.QImage(imageSize, QtGui.QImage.Format_ARGB32)
        self.imagePreview = QtGui.QImage(imageSize, QtGui.QImage.Format_ARGB32)
        self.lastPoint = QtCore.QPoint()        
        self.sizew = 800
        self.sizeh = 500


    def openImage(self, fileName):
        loadedImage = QtGui.QImage()
        if not loadedImage.load(fileName[0]):
            return False

        
        self.image = loadedImage.convertToFormat(QtGui.QImage.Format_RGB32)  
        self.sizeh = self.image.height()
        self.sizew = self.image.width()

        self.image = self.image.scaled(self.image.width()*.75, self.image.height()*.75)        
        self.sizew *= .75
        self.sizeh *= .75
        self.setMinimumSize(self.sizew, self.sizeh)
        self.setMaximumSize(self.sizew, self.sizeh)
        self.imagePreview = self.imagePreview.scaled(self.sizew, self.sizeh)

        self.image = self.image.scaled(self.image.width()*.75, self.image.height()*.75)        
        self.sizew *= .75
        self.sizeh *= .75
        self.setMinimumSize(self.sizew, self.sizeh)
        self.setMaximumSize(self.sizew, self.sizeh)
        self.imagePreview = self.imagePreview.scaled(self.sizew, self.sizeh)

        self.setMinimumSize(self.image.size())
        self.setMaximumSize(self.image.size())
        self.update()
        return True

    def saveImage(self, fileName, fileFormat):
        visibleImage = self.image

        if visibleImage.save(fileName, fileFormat):
            self.modified = False
            return True
        else:
            return False

    def setPenColor(self, newColor):
        self.pColor = newColor

    def setPenWidth(self, newWidth):
        self.pWidth = newWidth


    def zoomIn(self):
        self.image = self.image.scaled(self.image.width()*1.25, self.image.height()*1.25)
        self.sizew *= 1.25
        self.sizeh *= 1.25
        self.setMinimumSize(self.sizew, self.sizeh)
        self.setMaximumSize(self.sizew, self.sizeh)
        self.imagePreview = self.imagePreview.scaled(self.sizew, self.sizeh)
        self.update()

    def zoomOut(self):
        self.image = self.image.scaled(self.image.width()*.75, self.image.height()*.75)        
        self.sizew *= .75
        self.sizeh *= .75
        self.setMinimumSize(self.sizew, self.sizeh)
        self.setMaximumSize(self.sizew, self.sizeh)
        self.imagePreview = self.imagePreview.scaled(self.sizew, self.sizeh)
        self.update()
    
    def clearImage(self):
        self.image.fill(QtGui.qRgb(255, 255, 255))
        self.modified = True
        self.update()

    def clearImagePreview(self):
        self.imagePreview.fill(QtGui.qRgba(255, 255, 255, 0))

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.firstPoint_x = event.x()
            self.firstPoint_y = event.y()            
            self.scribbling = True

    def mouseMoveEvent(self, event):
        if (event.buttons() & QtCore.Qt.LeftButton) and self.scribbling:
            if self.tools['pen'] or self.tools['eraser']:
                self.draw(event.x(),event.y())                
            else:
                self.flag = False                
                self.drawPreview(event.x(), event.y())

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.scribbling:
            self.flag = True
            self.draw(event.x(),event.y())
            self.scribbling = False        
        
    def setTool(self, st):
        for i in self.tools:
            self.tools[i] = False            
        self.tools[st] = True                

    def paintEvent(self, event):        
        painter = QtGui.QPainter(self)        
        painter.drawImage(event.rect(), self.image)
        painter.drawImage(event.rect(), self.imagePreview)
        self.clearImagePreview()

    def draw(self, endPoint_x, endPoint_y):            
        
        painter = QtGui.QPainter(self.image)
        
        painter.setPen(QtGui.QPen(self.pColor, self.pWidth, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        painter.setClipping(True)
                    
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
        painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)                                            
        
        if self.tools['eraser']:
            painter.setPen(QtGui.QPen(QtCore.Qt.white, 10, QtCore.Qt.SolidLine))
            painter.drawLine(self.firstPoint_x, self.firstPoint_y, endPoint_x, endPoint_y)
            self.firstPoint_x = endPoint_x
            self.firstPoint_y = endPoint_y
                
        if self.tools['pen']:
            painter.drawLine(self.firstPoint_x, self.firstPoint_y, endPoint_x, endPoint_y)
            self.firstPoint_x = endPoint_x
            self.firstPoint_y = endPoint_y
                        
        if self.tools['line'] and self.flag:
            painter.drawLine(self.firstPoint_x,self.firstPoint_y, endPoint_x, endPoint_y)            
                                                
        self.modified = True
        self.update()

    def drawPreview(self, endPoint_x, endPoint_y):
                        
        painter = QtGui.QPainter(self.imagePreview)
        
        painter.setPen(QtGui.QPen(self.pColor, self.pWidth, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        painter.setClipping(True)
                    
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
        painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)        
        
        painter.setOpacity(0.4)
        
        if self.tools['line']:
            painter.drawLine(self.firstPoint_x, self.firstPoint_y, endPoint_x, endPoint_y)

        self.update()
    
    def mirror_h(self):
        self.image = self.image.mirrored(False, True)
        self.update()

    def mirror_w(self):
        self.image = self.image.mirrored(True, False)        
        self.update()
        
    

    def swapPixel(self):
        self.image = self.image.rgbSwapped()

    def resizeImage(self, image, newSize):
        if image.size() == newSize:
            return

        newImage = QtGui.QImage(newSize, QtGui.QImage.Format_RGB32)
        newImage.fill(QtGui.qRgb(255, 255, 255))
        painter = QtGui.QPainter(newImage)
        painter.drawImage(QtCore.QPoint(0, 0), image)
    
        self.image = newImage

    def isModified(self):
        return self.modified

    def penColor(self):
        return self.pColor

    def penWidth(self):
        return self.pWidth

