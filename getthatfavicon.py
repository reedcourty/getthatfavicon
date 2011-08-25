#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
A favicon downloader
"""

import urllib
import urlparse
import sys

import Image

class FaviconDownloader():
    def __init__(self, url):
        self.url = url
        up = urlparse.urlparse(self.url)
        self.favicon_url = up.scheme + '://' + up.netloc + '/favicon.ico'
        self.filename = sys.path[0] + '//favicon.' + up.netloc + '.ico'
        self.favicon = None
    
    def get_favicon_type(self):
        try:
            img = Image.open(self.filename)
        except IOError as error:
            if error[0] == "cannot identify image file":
                return 'NO_IMAGE'
        return img.format
        
        
    def get_favicon(self):
        print(self.favicon_url)
        (self.favicon, headers) = urllib.urlretrieve(self.favicon_url, self.filename)
        print(self.favicon, headers)
        if self.get_favicon_type() != 'ICO':
            print(self.filename + " isn't an icon file.")
        
        
if __name__ == '__main__':
    fd = FaviconDownloader('http://docs.python.org')
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
