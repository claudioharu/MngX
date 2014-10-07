from PySide import QtCore, QtGui

import sys
import os
import urllib
import glob
import shutil
import re
from zipfile import ZipFile
try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup
from contextlib import closing
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
from itertools import islice


class Thread(QtCore.QThread):

    #This is the signal that will be emitted during the processing.
    #By including int as an argument, it lets the signal know to expect
    #an integer argument when emitting.
    notifyProgress = QtCore.Signal(int)

    #You can do any extra things in this init you need, but for this example
    #nothing else needs to be done expect call the super's init
    def __init__(self, parent=None):
        self.URL_BASE = "http://mangafox.me/"
        self.i = 1.
        super (Thread, self).__init__(parent)

    # QtCore.QThread.__init__(self)

    #A QThread is run by calling it's start() function, which calls this run()
    #function in it's own "thread". 
    def setTitle(self,title):
        self.title = title

    def run(self):
        # print self
        # for i in range (0,101):
        #     self.notifyProgress.emit(i)
        self.downloadMangas(self.title)

    def get_page_soup(self,url):
        """Download a page and return a BeautifulSoup object of the html"""
        with closing(urllib.urlopen(url)) as html_file:
            return BeautifulSoup(html_file.read())


    def getChapterUrls(self, manga_name):
        """Get the chapter list for a manga"""
        replace = lambda s, k: s.replace(k, '_')
        manga_url = reduce(replace, [' ', '-'], manga_name.lower())
        url = '{0}manga/{1}'.format(self.URL_BASE, manga_url)
        # print('Url: ' + url)
        soup = self.get_page_soup(url)
        manga_does_not_exist = soup.find('form', {'id': 'searchform'})
        if manga_does_not_exist:
            search_sort_options = 'sort=views&order=za'
            url = '{0}/search.php?name={1}&{2}'.format(self.URL_BASE, manga_url, search_sort_options)
            soup = self.get_page_soup(url)
            results = soup.findAll('a', {'class': 'series_preview'})
            error_text = 'Error: Manga \'{0}\' does not exist'.format(manga_name)
            error_text += '\nDid you meant one of the following?\n  * '
            error_text += '\n  * '.join([manga.text for manga in results][:10])
            sys.exit(error_text)
        warning = soup.find('div', {'class': 'warning'})
        if warning and 'licensed' in warning.text:
            sys.exit('Error: ' + warning.text)
        chapters = OrderedDict()
        links = soup.findAll('a', {'class': 'tips'})
        if(len(links) == 0):
            sys.exit('Error: Manga either does not exist or has no chapters')
        replace_manga_name = re.compile(re.escape(manga_name.replace('_', ' ')), re.IGNORECASE)
        for link in links:
            chapters[replace_manga_name.sub('', link.text).strip()] = link['href']
        return chapters


    def getPagesNumbers(self,soup):
        # """Return the list of page numbers from the parsed page"""
        raw = soup.findAll('select', {'class': 'm'})[0]
        return (html['value'] for html in raw.findAll('option'))


    def getChaptersImageUrls(self,url_fragment):
        """Find all image urls of a chapter and return them"""
        print('Getting chapter urls')
        url_fragment = os.path.dirname(url_fragment) + '/'
        chapter_url = url_fragment
        chapter = self.get_page_soup(chapter_url)
        pages = self.getPagesNumbers(chapter)
        image_urls = []
        print('Getting image urls...')
        for page in pages:
            # print('url_fragment: {0}'.format(url_fragment))
            # print('page: {0}'.format(page))
            # print('Getting image url from {0}{1}.html'.format(url_fragment, page))
            page_soup = self.get_page_soup(chapter_url + page + '.html')
            images = page_soup.findAll('img', {'id': 'image'})
            if images:
                image_urls.append(images[0]['src'])
        return image_urls


    def getChaptersNumber(self,url_fragment):
        """Parse the url fragment and return the chapter number."""
        return ''.join(url_fragment.rsplit("/")[5:-1])


    def downloadUrls(self,image_urls, manga_name, chapter_number):
        """Download all images from a list"""
        download_dir = '{0}/{1}/'.format(manga_name, chapter_number)
        if os.path.exists(download_dir):
            shutil.rmtree(download_dir)
        os.makedirs(download_dir)
        for i, url in enumerate(image_urls):
            filename = './{0}/{1}/{2:03}.jpg'.format(manga_name, chapter_number, i)
            # print('Downloading {0} to {1}'.format(url, filename))
            urllib.urlretrieve(url, filename)

    def downloadMangas(self, manga_name, chapter_number=None):
        """Download all chapters of a manga"""
        chapter_urls = self.getChapterUrls(manga_name)
        self.total = len(chapter_urls)
        print "total " + str(self.total)
        self.i = 1.
        for chapter_number, url_fragment in chapter_urls.iteritems():
            chapter_number = self.getChaptersNumber(url_fragment)
            # print('===============================================')
            # print('Chapter ' + chapter_number)
            # print('===============================================')
            image_urls = self.getChaptersImageUrls(url_fragment)
            self.downloadUrls(image_urls, manga_name, chapter_number)
            download_dir = './{0}/{1}'.format(manga_name, chapter_number)
            value = (self.i/self.total)*100.
            self.notifyProgress.emit(int(value))
            self.i += 1
            print "chapter " + str(self.i) + " downloaded"
        