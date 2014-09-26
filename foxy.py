# -*- coding: utf-8 -*-
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from urlparse import urljoin
import os
import glob
import argparse
import shutil
from zipfile import ZipFile
import progress
from PySide import QtCore, QtGui

class MangaChapter(object):
    '''Contains information about single chapter of mangs'''
    def __init__(self, manga_title, volume, chapter_number, pages_count):
        self.manga_title = manga_title
        self.volume = volume
        print self.volume
        self.chapter_number = chapter_number
        self.pages_count = pages_count
        self.pages = {}

        self.storage_dir = ''
        self.filename_pattern = ''
        self.downloaded_images_count = 0


class MangafoxSpider(BaseSpider, QtGui.QWidget):
    name = 'mangafox'
    base_url = 'http://www.mangafox.com/manga/'

    def __init__(self, title):
        self.title = title
        self.count = 0
        QtGui.QWidget.__init__(self, None)

        self.prog = QtGui.QProgressBar(self) 
        self.prog.setProperty("value", 0)

    def start_requests(self):
        return [Request(urljoin(self.base_url, self.title), callback=self.parse_chapters_list)]

    def parse_chapters_list(self, response):
        hxs = HtmlXPathSelector(response)
        chapters = hxs.select('//a[@class="tips"]/@href').extract()
        self.totalChapt = len(chapters)

        if not chapters:
            print 'Can not find manga series with specified title.'
            return

        print 'Found %s chapters of %s manga series' % (len(chapters), self.title)

        reqs = []
        chapters.sort()
        for url in chapters:
            reqs.append(Request(url, callback=self.parse_chapter_contents))
        return reqs

    def parse_chapter_contents(self, response):
        hxs = HtmlXPathSelector(response)
        pages_count_raw = hxs.select('//select[@class="m"]')[0].select('count(option)').extract()[0]
        pages_count = int(float(pages_count_raw))

        volume, chapter_number = response.url.split('/')[-3: -1]
        chapter = MangaChapter(self.title, volume, chapter_number, pages_count)
        print 'Chapter %s of volume %s consists of %s pages. Rerieving urls of pages images...' % (chapter_number, volume, pages_count)


        reqs = []
        for page in range(1, pages_count + 1):
            page_url = urljoin(response.url, '%s.html' % page)
            page_request = Request(page_url, callback=self.parse_chapter_page, dont_filter=True)
            page_request.meta['chapter'] = chapter
            page_request.meta['page_number'] = page
            reqs.append(page_request)
        return reqs

    def parse_chapter_page(self, response):
        hxs = HtmlXPathSelector(response)
        chapter = response.meta['chapter']
        page_number = response.meta['page_number']

        image_url = hxs.select('id("image")/@src').extract()[0]

        chapter.pages[page_number] = image_url
        if len(chapter.pages) == chapter.pages_count:
            #Sinal de progresso incrementado
            print 'All urls of chapter %s of volume %s retrieved. Starting download...' % (chapter.chapter_number, chapter.volume)
            # brave_10/brave_10_v01/brave_10_v01_c01/brave_10_v01_c001_p001.jpg
            chapter_dir_name = chapter.chapter_number
            #volume_dir_name = '%s_%s' % (self.title, chapter.volume)
            #chapter_dir_name = '%s_%s' % (volume_dir_name, chapter.chapter_number) #(volume_dir_name, chapter.chapter_number) 
            chapter_dir = os.path.join(self.title, chapter_dir_name) #((self.title, volume_dir_name, chapter_dir_name))

            chapter.storage_dir = chapter_dir
            chapter.filename_pattern = '%03d.jpg' #chapter_dir_name + '_p%03d.jpg'

            if os.path.exists(chapter_dir):
                shutil.rmtree(chapter_dir)
            os.makedirs(chapter_dir)

            reqs = []
            for page, image_url in chapter.pages.iteritems():
                page_image_request = Request(image_url, callback=self.process_page_image)
                page_image_request.meta['chapter'] = chapter
                page_image_request.meta['page_number'] = page
                reqs.append(page_image_request)

            self.count += 1
            self.prog.setValue((self.count*100)/self.totalChapt)
            return reqs

    def process_page_image(self, response):
        #print "oi"
        chapter = response.meta['chapter']
        page_number = response.meta['page_number']
        filename = os.path.join(chapter.storage_dir, chapter.filename_pattern % page_number)
        with open(filename, 'wb') as f:
            f.write(response.body)

        chapter.downloaded_images_count += 1
        #print chapter.downloaded_images_count, chapter.pages_count
        if chapter.downloaded_images_count == chapter.pages_count -1:
            print 'Chapter %s successfully downlaoded to %s.' % (chapter.chapter_number, chapter.storage_dir)

            # print 'Making CBZ...'
            # makecbz(chapter.storage_dir)


def makecbz(dirname):
    '''Create CBZ files for all files in a directory.'''
    dirname = os.path.abspath(dirname)
    zipname = dirname + '.cbz'
    images = glob.glob(dirname + '/*.jpg')
    myzip = ZipFile(zipname, 'w')
    for filename in images:
        #print 'Writing %s to %s' % (filename, zipname)
        myzip.write(filename)
    myzip.close()


def create_crawler(spider):
    '''Setups item signal and run the spider'''
    from scrapy import signals
    from scrapy.xlib.pydispatch import dispatcher

    def catch_item(sender, item, **kwargs):
        print "Got:", item

    dispatcher.connect(catch_item, signal=signals.item_passed)

    # shut off log
    from scrapy.conf import settings
    settings.overrides['LOG_ENABLED'] = False

    # set up crawler
    from scrapy.crawler import CrawlerProcess

    crawler = CrawlerProcess(settings)
    crawler.install()
    crawler.configure()

    # schedule spider
    crawler.crawl(spider)

    return crawler


def main():
    # parser = argparse.ArgumentParser(description='Downloads manga from Mangafox.')
    # parser.add_argument('title', help='Title of the manga series to download.')
    # params = parser.parse_args()
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

if __name__ == '__main__':
    main()