from PySide import QtCore, QtGui
from foxy import *

class Thread(QtCore.QThread):

    #This is the signal that will be emitted during the processing.
    #By including int as an argument, it lets the signal know to expect
    #an integer argument when emitting.


    #You can do any extra things in this init you need, but for this example
    #nothing else needs to be done expect call the super's init
    def __init__(self, parent=None):
        super (Thread, self).__init__(parent)
        # QtCore.QThread.__init__(self)

    #A QThread is run by calling it's start() function, which calls this run()
    #function in it's own "thread". 
    def setTitle(self,title):
        self.title = title

    def spiderCreat(self):
        self.spider = MangafoxSpider(self.title)
    def crawlerCreat(self):
        self.crawler = create_crawler(self.spider)

    def run(self):
        print self
        self.spiderCreat()
        self.spider.show()
        self.crawlerCreat()
        #self.emit(QtCore.SIGNAL("progress(int)"), spider.percent)
        # start engine scrapy/twisted
        print 'Starting'
        self.crawler.start()
        print 'Successfully completed. Stopping.'