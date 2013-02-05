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
import sys

import Image
import requests
from bs4 import BeautifulSoup

# Some test cases:
#
# - index.hu (Multiple icon)
# - twitter.com (CDN)
# - otp.hu (Redirecting)
# - worldoftanks.eu (Default domain/favicon.ico, no HTML link)
# - facebook.com
# - projecteuler.com (Wrong TLD)

test_pages = ['index.hu', 'twitter.com', 'otp.hu', 'worldoftanks.eu', 'facebook.com', 'projecteuler.com']

def debug_print(var_str, var):
    if DEBUG:
        now = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        print("DEBUG -- {0} -- {1} = {2}".format(now, var_str, var))

class FaviconDownloader():

    def get_full_url(self):
        up = urlparse.urlparse(self.url)
        if (up.scheme == ''):
            self.full_url = 'http://' + self.url
            
        debug_print('get_full_url > self.full_url', self.full_url)
        
    def set_page_url(self):
        up = urlparse.urlparse(self.url)
        
        debug_print('set_page_url > up', up)
        
        if (up.scheme == ''):
            self.page_url = 'http://' + self.url
        else:
            self.page_url = self.url
            
        debug_print('set_page_url > self.page_url', self.page_url)
        

    def __init__(self, url):
        self.url = url
        debug_print('fd.url', self.url)
        
        self.page_url = None
        self.set_page_url()
        debug_print('fd.page_url', self.page_url)
        
        self.full_url = None
        self.get_full_url()
        debug_print('fd.full_url', self.full_url)
        
        self.favicon_url = None
        debug_print('fd.favicon_url', self.favicon_url)
        
        self.filename = None
        debug_print('fd.filename', self.filename)
        
        self.icon = None
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
        
        debug_print('is_valid_favicon > img', img)
        
        if img == None:
            return False
        if img.format == 'ICO' or img.format == 'PNG':
            return True
        else:
            return False
            
    def get_favicon_type(self):
        img = self.get_img()
        
        debug_print('get_favicon_type > img', img)
        
        if img == None:
            return 'ERROR'
        if img.format == 'ICO':
            return 'ICO'
        if img.format == 'PNG':
            return 'PNG'
            
    def get_favicon_urls(self):
        
        self.get_full_url()
        
        try:
            r = requests.get(self.full_url)
        except requests.exceptions.ConnectionError as e:
            print('Connection error!')
            if DEBUG:
                print("The error was: {0}".format(e))
            sys.exit()
        
        debug_print('get_favicon_urls > r', r)
        
        soup = BeautifulSoup(r.text.encode('utf-8'))
        
        debug_print('get_favicon_urls > soup', soup)
        
        try:
            icons = soup.head.find_all(rel="icon")
            debug_print('get_favicon_url > icons', icons)
        except AttributeError as e:
            if DEBUG:
                print("Possible redirecting...")
            debug_print('get_favicon_urls > r', r.content)
            if r.content.find("Refresh"):
                self.full_url = r.content[r.content.find("URL=")+4:len(r.content)]
                self.full_url = self.full_url[0:self.full_url.find('"')]
            
            debug_print('get_favicon_urls > self.url', self.url)
            debug_print('get_favicon_urls > self.full_url', self.full_url)
            
            try:
                r = requests.get(self.full_url)
            except requests.exceptions.MissingSchema as e:
                print("Something went wrong! :( {0}".format(e))
                sys.exit()
        
            debug_print('get_favicon_urls > r', r)
        
            soup = BeautifulSoup(r.text.encode('utf-8'))
            try:
                icons = soup.head.find_all(rel="icon")
            except AttributeError as e:
                print("Error")
                
        self.favicon_url = [self.full_url + "/favicon.ico"]
        
        for icon in icons:
            debug_print('get_favicon_urls > icon[\'href\']', icon['href'])
                
            up = urlparse.urlparse(icon['href'])
            
            debug_print('get_favicon_urls > up', up)
                
            if (up.scheme == ''):
                url_scheme = 'http'
            else:
                url_scheme = up.scheme
                
            if (up.netloc == ''):
                url_netloc = urlparse.urlparse(self.full_url).netloc
            else:
                url_netloc = up.netloc
                
            favicon = url_scheme + "://" + url_netloc + up.path
            
            debug_print('get_favicon_urls > favicon', favicon)
            
            self.favicon_url.append(favicon)
        
        debug_print('get_favicon_urls > self.favicon_url', self.favicon_url)
    
    def save_favicon(self):
        if (os.path.exists(self.filename)):
            now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            self.filename = self.filename + "." + now + "." + self.get_favicon_type().lower()
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
                
                up = urlparse.urlparse(self.full_url)
                
                debug_print('get_favicon > up', up)
                
                if (t[len(t)-1] == 'favicon.ico' or t[len(t)-1] == 'favicon.png'):
                    self.filename = "favicon." + up.netloc + "." + self.get_favicon_type().lower()
                else:
                    self.filename = "favicon." + up.netloc + "-" + t[len(t)-1] + "." + self.get_favicon_type().lower()
                
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
    parser.add_argument('--test', action="store_true", default=False, help='Switch on the test mode.')
    
    args = parser.parse_args()
    
    if args.test:
        DEBUG = True
        for p in test_pages:
            fd = FaviconDownloader(p)
            fd.get_favicon_urls()
            fd.get_favicon()
    
    if args.debug:
        DEBUG = True
    
    fd = FaviconDownloader(args.url)
    fd.get_favicon_urls()
    fd.get_favicon()

    