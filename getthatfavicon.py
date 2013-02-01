#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
A favicon downloader
"""

import urlparse
import os.path
import argparse
import StringIO
import datetime

import Image
import requests
from bs4 import BeautifulSoup

def debug_print(var_str, var):
    now = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
    print("DEBUG -- {0} -- {1} = {2}".format(now, var_str, var))

class FaviconDownloader():
    def __init__(self, url):
        self.url = url
        self.favicon_url = None
        self.filename = None
        self.icon = None
        if DEBUG:
            debug_print('fd.url', self.url)
            debug_print('fd.favicon_url', self.favicon_url)
            debug_print('fd.filename', self.filename)
            debug_print('fd.icon', self.icon)
    
    def get_img(self):
        output = StringIO.StringIO(self.icon)
                
        try:
            img = Image.open(output)
            output.close()
            return img
        except IOError as error:
            if error[0] == "cannot identify image file":
                return None
    
    def is_valid_favicon(self):
        img = self.get_img()
        
        if DEBUG:
            debug_print('is_valid_favicon > img', img)
        
        if img == None:
            return False
        if img.format == 'ICO' or img.format == 'PNG':
            return True
        else:
            return False
            
    def get_favicon_type(self):
        img = self.get_img()
        
        if DEBUG:
            debug_print('get_favicon_type > img', img)
        
        if img == None:
            return 'ERROR'
        if img.format == 'ICO':
            return 'ICO'
        if img.format == 'PNG':
            return 'PNG'
            
    def get_favicon_url(self):
        
        up = urlparse.urlparse(self.url)
        if (up.scheme == ''):
            self.url = 'http://' + self.url
            
        if DEBUG:
            debug_print('get_favicon_url > self.url', self.url)
                
        r = requests.get(self.url)
        
        if DEBUG:
            debug_print('get_favicon_url > r', r)
        
        soup = BeautifulSoup(r.text.encode('utf-8'))
        
        try:
            icons = soup.head.find_all(rel="icon")
        except AttributeError as e:
            if DEBUG:
                print("Possible redirecting...")
                debug_print('get_favicon_url > r', r.content)
            if r.content.find("Refresh"):
                self.url = r.content[r.content.find("URL=")+4:len(r.content)]
                self.url = self.url[0:self.url.find('"')]
            if DEBUG:
                debug_print('get_favicon_url > self.url', self.url)
            r = requests.get(self.url)
        
            if DEBUG:
                debug_print('get_favicon_url > r', r)
        
            soup = BeautifulSoup(r.text.encode('utf-8'))
            try:
                icons = soup.head.find_all(rel="icon")
            except AttributeError as e:
                print("Error")
                
        self.favicon_url = []
        
        for icon in icons:
            if DEBUG:
                debug_print('get_favicon_url > icon[\'href\']', icon['href'])
                
            up = urlparse.urlparse(icon['href'])
            
            if DEBUG:
                debug_print('get_favicon_url > up', up)
                
            if (up.scheme == ''):
                url_scheme = 'http'
            else:
                url_scheme = up.scheme
                
            if (up.netloc == ''):
                url_netloc = urlparse.urlparse(self.url).netloc
            else:
                url_netloc = up.netloc
                
            favicon = url_scheme + "://" + url_netloc + up.path
            
            if DEBUG:
                debug_print('get_favicon_url > favicon', favicon)
            
            self.favicon_url.append(favicon)
        
        if DEBUG:
            debug_print('get_favicon_url > self.favicon_url', self.favicon_url)
    
    def save_favicon(self):
        if (os.path.exists(self.filename)):
            now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            self.filename = self.filename + "." + now + "." + self.get_favicon_type().lower()
        if DEBUG:
            debug_print('save_favicon > self.filename', self.filename)
        print(u"Saving {0} ...".format(self.filename))
        with open(self.filename,"wb") as f:
            f.write(self.icon)
    
    def get_favicon(self):
        if (len(self.favicon_url) > 0):
            for fu in self.favicon_url:
                print("\nDownloading {0} ...".format(fu))
                r = requests.get(fu)
                
                self.icon = r.content
                           
                t = fu.split("/")
                
                up = urlparse.urlparse(self.url)
                
                if DEBUG:
                    debug_print('get_favicon > up', up)
                
                if (t[len(t)-1] == 'favicon.ico' or t[len(t)-1] == 'favicon.png'):
                    self.filename = "favicon." + up.netloc + "." + self.get_favicon_type().lower()
                else:
                    self.filename = "favicon." + up.netloc + "-" + t[len(t)-1] + "." + self.get_favicon_type().lower()
                
                if DEBUG:
                    debug_print('get_favicon > self.filename', self.filename)
                
                if self.is_valid_favicon():
                    self.save_favicon()
                else:
                    print("Wrong icon!")
        else:
            print("The page hasn't got favicon!")

if __name__ == '__main__':
    
    DEBUG = False
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('url', help='The URL of that page which has that nice favicon.')
    parser.add_argument('--debug', action="store_true", default=False, help='Switch on the debug mode.')
    args = parser.parse_args()
    
    if args.debug:
       DEBUG = True
    
    fd = FaviconDownloader(args.url)
    fd.get_favicon_url()
    fd.get_favicon()

    