#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
A favicon downloader
"""

import urllib
import urlparse
import sys
import os
import argparse
import StringIO

import Image

import requests
from bs4 import BeautifulSoup

class FaviconDownloader():
    def __init__(self, url):
        self.url = url
        self.favicon_url = None
        self.filename = None
    
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
            
    def get_favicon_type(self):
    
        output = StringIO.StringIO(self.icon)
                
        try:
            img = Image.open(output)
            output.close()
        except IOError as error:
            if error[0] == "cannot identify image file":
                return None
        if img.format == 'ICO':
            return 'ICO'
        if img.format == 'PNG':
            return 'PNG'
            
    def get_favicon_url(self):
        
        up = urlparse.urlparse(self.url)
        if (up.scheme == ''):
            self.url = 'http://' + self.url
                
        r = requests.get(self.url)

        soup = BeautifulSoup(r.text.encode('utf-8'))
        icons = soup.head.find_all(rel="icon")
        
        self.favicon_url = []
        
        for icon in icons:
            if (icon['href'].find("://") == -1):
                favicon = self.url + icon['href']
            else:
                favicon = icon['href']
            self.favicon_url.append(favicon)
        
    def get_favicon(self):
        for fu in self.favicon_url:
            print("\n" + fu)
            r = requests.get(fu)
            
            self.icon = r.content
                       
            t = fu.split("/")
            filename = "favicon." + self.url.split("//")[1] + "." + t[len(t)-1] + "." + self.get_favicon_type().lower()
            print(filename)
            with open(filename,"wb") as f:
                f.write(r.content)  

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    
    parser.add_argument('url', help='The URL of that page which has that nice favicon.')
    args = parser.parse_args()
    
    fd = FaviconDownloader(args.url)
    fd.get_favicon_url()
    fd.get_favicon()

    