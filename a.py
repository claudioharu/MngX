import sys
   2 from PyQt4.QtCore import *
   3 from PyQt4.QtGui import *
   4 
   5 if __name__ == "__main__":
   6 
   7     app = QApplication(sys.argv)
   8     
   9     if len(app.arguments()) < 2:
  10     
  11         sys.stderr.write("Usage: %s <image file> <overlay file>\n" % sys.argv[0])
  12         sys.exit(1)
  13     
  14     image = QImage(app.arguments()[1])
  15     if image.isNull():
  16         sys.stderr.write("Failed to read image: %s\n" % app.arguments()[1])
  17         sys.exit(1)
  18     
  19     overlay = QImage(app.arguments()[2])
  20     if overlay.isNull():
  21         sys.stderr.write("Failed to read image: %s\n" % app.arguments()[2])
  22         sys.exit(1)
  23     
  24     if overlay.size() > image.size():
  25     
  26         overlay = overlay.scaled(image.size(), Qt.KeepAspectRatio)
  27     
  28     painter = QPainter()
  29     painter.begin(image)
  30     painter.drawImage(0, 0, overlay)
  31     painter.end()
  32     
  33     label = QLabel()
  34     label.setPixmap(QPixmap.fromImage(image))
  35     label.show()
  36     
  37     sys.exit(app.exec_())
