from PySide import QtCore, QtGui
import os
import sys
import glob

def supported_image_extensions():
    ''' Get the image file extensions that can be read. '''
    formats = QtGui.QImageReader().supportedImageFormats()
    # Convert the QByteArrays to strings
    return [str(fmt) for fmt in formats]

class ImageFileList(QtGui.QListWidget):
    ''' A specialized QListWidget that displays the
        list of all image files in a given directory. '''
 
    def __init__(self, dirpath, parent=None):
        QtGui.QListWidget.__init__(self, parent)
        # print(dirpath)
        self.setDirpath(dirpath)
 
 
    def setDirpath(self, dirpath):
        ''' Set the current image directory and refresh the list. '''
        self._dirpath = dirpath
        self._populate()
 
 
    def _images(self):
        ''' Return a list of filenames of all
            supported images in self._dirpath. '''
 
        # Start with an empty list
        images = []
 
        # Find the matching files for each valid
        # extension and add them to the images list
        for extension in supported_image_extensions():
            pattern = os.path.join(self._dirpath,
                                   '*.%s' % extension)
            print glob.glob(pattern)
            images.extend(glob.glob(pattern))
        
        # 
        images.sort()
        return images
 
 
    def _populate(self):
        ''' Fill the list with images from the
            current directory in self._dirpath. '''
 
        # In case we're repopulating, clear the list
        self.clear()
 
        # Create a list item for each image file,
        # setting the text and icon appropriately
        for image in self._images():
            item = QtGui.QListWidgetItem(self)
            #item.setText(image)
            item.setIcon(QtGui.QIcon(image))

if __name__ == '__main__':
	# The app doesn't receive sys.argv, because we're using
	# sys.argv[1] to receive the image directory
	app = QtGui.QApplication([])

	# Create a window, set its size, and give it a layout
	win = QtGui.QWidget()
	win.setWindowTitle('Image List')
	win.setMinimumSize(600, 400)
	layout = QtGui.QVBoxLayout()
	win.setLayout(layout)

	# Create one of our ImageFileList objects using the image
	# directory passed in from the command line
	lst = ImageFileList(sys.argv[1], win)

	layout.addWidget(lst)

	entry = QtGui.QLineEdit(win)

	layout.addWidget(entry)

	def on_item_changed(curr, prev):
		entry.setText(curr.text())

	lst.currentItemChanged.connect(on_item_changed)

	win.show()
	app.exec_()
