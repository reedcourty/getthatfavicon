#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
A favicon downloader
"""

import urllib
import urlparse
import sys
import os

import Image

class FaviconDownloader():
    def __init__(self, url):
        self.url = url
        self.up = urlparse.urlparse(self.url)
        self.favicon_url = self.up.scheme + '://' + self.up.netloc + '/favicon.ico'
        self.filename = sys.path[0] + '//favicon.' + self.up.netloc + '.ico'
        self.favicon = None
    
    def is_valid_favicon(self):
        try:
            img = Image.open(self.filename)
        except IOError as error:
            if error[0] == "cannot identify image file":
                return False
        if img.format == 'ICO' or img.format == 'PNG':
            return True
        else:
            return False
        
    def get_favicon(self):
        print(self.favicon_url)
        (self.favicon, headers) = urllib.urlretrieve(self.favicon_url, self.filename)
        print(self.favicon, headers)
        if not self.is_valid_favicon():
            print(self.filename + " isn't a valid favicon.")
            os.remove(self.filename)
            new_url = self.up.scheme + '://' + self.up.netloc[((self.up.netloc.find('.'))+1):]
            new_fd = FaviconDownloader(new_url)
            print(fd)
            new_fd.get_favicon()        
        
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
