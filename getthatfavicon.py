#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
A favicon downloader
"""

import urllib
import urlparse
import sys

class FaviconDownloader():
    def __init__(self, url):
        self.url = url
        up = urlparse.urlparse(self.url)
        self.netloc = up.netloc
        self.favicon_url = up.scheme + '://' + self.netloc + '/favicon.ico'
        self.favicon = None
        
    def get_favicon(self):
        filename = sys.path[0] + '//favicon.' + self.netloc + '.ico'
        print(self.favicon_url)
        (self.favicon, headers) = urllib.urlretrieve(self.favicon_url, filename)
        print(self.favicon, headers)
        
if __name__ == '__main__':
    fd = FaviconDownloader('http://python.org')
    print(fd)
    fd.get_favicon()
    fd = FaviconDownloader('http://www.google.com')
    print(fd)
    fd.get_favicon()
    fd = FaviconDownloader('https://github.com/reedcourty/getthatfavicon')
    print(fd)
    fd.get_favicon()
    fd = FaviconDownloader('http://www.doodle.com/73hqnfzzkbmnqeqa')
    print(fd)
    fd.get_favicon()
