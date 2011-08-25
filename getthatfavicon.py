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
        up = urlparse.urlparse(self.url)
        if (up.scheme == ''):
            self.scheme = 'http'
        else:
            self.scheme = up.scheme
        if (up.netloc == ''):
            self.netloc = up.path
        else:
            self.netloc = up.netloc
        self.favicon_url = self.scheme + '://' + self.netloc + '/favicon.ico'
        self.filename = sys.path[0] + '//favicon.' + self.netloc + '.ico'
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
        print("\n" + self.favicon_url)
        (self.favicon, headers) = urllib.urlretrieve(self.favicon_url, self.filename)
        print(self.favicon)
        if not self.is_valid_favicon():
            print(self.filename + " isn't a valid favicon.")
            os.remove(self.filename)
            new_url = self.scheme + '://' + self.netloc[((self.netloc.find('.'))+1):]
            new_fd = FaviconDownloader(new_url)
            new_fd.get_favicon()
        
if __name__ == '__main__':
    fd = FaviconDownloader('http://docs.python.org')
    fd.get_favicon()
    fd = FaviconDownloader('http://www.google.com')
    fd.get_favicon()
    fd = FaviconDownloader('https://github.com/reedcourty/getthatfavicon')
    fd.get_favicon()
    fd = FaviconDownloader('http://www.doodle.com/73hqnfzzkbmnqeqa')
    fd.get_favicon()
    fd = FaviconDownloader('http://translate.google.com/?hl=en#en|hu|added%20%22try%20until%20we%20find%20it%22%20feature.%20When%20the%20downloaded%20favicon%20isn%27t%20really%20an%20icon%20we%20try%20to%20find%20it%20an%20upper%20dns%20level.')
    fd.get_favicon()
    fd = FaviconDownloader('ratucen.sch.bme.hu')
    fd.get_favicon()
    