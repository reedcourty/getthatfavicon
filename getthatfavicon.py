#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
A favicon downloader
"""

import urllib
import sys

class FaviconDownloader():
    def __init__(self, url):
        self.url = url
        self.favicon = None
        
    def get_favicon(self):
        filename = sys.path[0] + '//favicon.ico'
        (self.favicon, headers) = urllib.urlretrieve(self.url, filename)
        print(self.favicon, headers)
        
if __name__ == '__main__':
    fd = FaviconDownloader('http://python.org/favicon.ico')
    print(fd)
    fd.get_favicon()
