from foxy import *


import os

def child():
	print 'A new child ',  os.getpid( )
	import sys
	app = QtGui.QApplication(sys.argv)

	# ex.showFullScreen()

	spider = MangafoxSpider("tenkuu_shinpan")
	spider.show()
	crawler = create_crawler(spider)

	# start engine scrapy/twisted
	print 'Starting'
	crawler.start()
	print 'Successfully completed. Stopping.'
	sys.exit(app.exec_())
	os._exit(0)  

def parent():

	newpid = os.fork()
	if newpid == 0:
		child()
	else:
		pids = (os.getpid(), newpid)
		print "parent: %d, child: %d" % pids

parent()