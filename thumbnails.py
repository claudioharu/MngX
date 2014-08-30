from PySide import QtCore, QtGui
import os
import sys
import glob

# def supported_image_extensions():
#     ''' Get the image file extensions that can be read. '''
#     formats = QtGui.QImageReader().supportedImageFormats()
#     # Convert the QByteArrays to strings
#     return [str(fmt) for fmt in formats]

class ImageFileList(QtGui.QListWidget):
    ''' A specialized QListWidget that displays the
        list of all image files in a given directory. '''
 
    def __init__(self, dirpath, parent=None):
        QtGui.QListWidget.__init__(self, parent)
        # print(dirpath)
        self.setMinimumWidth(self.sizeHintForColumn(0))
        self.setIconSize(QtCore.QSize(250,250))
        self.setDirpath(dirpath)

        self.setStyleSheet( """ QListWidget:item:selected {
                                    background-color: #f07645;
                                }
                                QListWidget:item {
                                    background-color: #a8a8a4;
                                }
                                QListWidget {
                                    background-color: #a8a8a4;

                                }

                                """
                                )

 
 
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
        pattern = os.path.join(self._dirpath,'*.jpg')
        #print glob.glob(pattern)
        images.extend(glob.glob(pattern))
        
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
            item.setIcon(QtGui.QIcon(image))
            #item.setBackground(QtCore.Qt.gray)
            #item.setSizeHint()