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
import logging

import Image
import requests
from bs4 import BeautifulSoup

import frequests

# Some test cases:
#
# - index.hu (Multiple icon)
# - twitter.com (CDN)
# - otp.hu (Redirecting)
# - worldoftanks.eu (Default domain/favicon.ico, no HTML link)
# - facebook.com
# - 750g.com (Downloading http://750g.comimgT/favicon.ico ...)
# - projecteuler.com (Wrong TLD)

test_pages = ['index.hu', 'twitter.com', 'otp.hu', 'worldoftanks.eu', 'facebook.com', '750g.com', 'projecteuler.com']

class FaviconDownloader():

    def get_full_url(self):
        up = urlparse.urlparse(self.url)
        logger.debug('get_full_url() -> up = {}'.format(up))
        logger.debug('get_full_url() -> up.scheme = {}'.format(up.scheme))
        if (up.scheme == ''):
            logger.debug('get_full_url() -> self.url = {}'.format(self.url))
            self.full_url = 'http://' + self.url
        else:
            self.full_url = self.url
        logger.debug('get_full_url() -> self.full_url = {0}'.format(self.full_url))
        
    def set_page_url(self):
        up = urlparse.urlparse(self.url)
        
        logger.debug('set_page_url -> up = {0}'.format(up))
        
        if (up.scheme == ''):
            self.page_url = 'http://' + self.url
        else:
            self.page_url = self.url
            
        logger.debug('set_page_url -> self.page_url = {0}'.format(self.page_url))
        

    def __init__(self, url):
        self.url = url
        logger.debug('__init__ -> self.url = {0}'.format(self.url))
        
        self.page_url = None
        logger.debug('__init__ -> self.set_page_url()')
        self.set_page_url()
        logger.debug('__init__ -> self.page_url = {0}'.format(self.page_url))
        
        self.full_url = None
        logger.debug('__init__ -> self.get_full_url()')
        self.get_full_url()
        logger.debug('__init__ -> self.full_url = {0}'.format(self.full_url))
        
        self.favicon_url = None
        logger.debug('__init__ -> self.favicon_url = {0}'.format(self.favicon_url))
        
        self.filename = None
        logger.debug('__init__ -> self.filename = {0}'.format(self.filename))
        
        self.icon = None
        logger.debug('__init__ -> self.icon = {0}'.format(self.icon))
        
    
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
        
        logger.debug('is_valid_favicon -> img = {0}'.format(img))
                
        if img == None:
            return False
        
        logger.debug('is_valid_favicon -> img.format = {0}'.format(img.format))
        
        if img.format == 'ICO' or img.format == 'PNG':
            return True
        else:
            return False
            
    def get_favicon_type(self):       
        img = self.get_img()
        
        logger.debug('get_favicon_type -> img = {0}'.format(img))
        
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
            logger.info('Connection error!')
            logger.debug('get_favicon_urls : The connection error was: {0}'.format(e))
            sys.exit()
        
        logger.debug('get_favicon_urls -> r = {0}'.format(r))
                
        soup = BeautifulSoup(r.text.encode('utf-8'))
        
        logger.debug('get_favicon_urls -> soup = {0}'.format(soup))
                
        try:
            icons = soup.head.find_all(rel="icon")
            logger.debug('get_favicon_urls -> icons = {0}'.format(icons))
        except AttributeError as e:
            logger.debug('get_favicon_urls : Possible redirecting...')
            logger.debug('get_favicon_urls -> r.content = {0}'.format(r.content))
            if r.content.find("Refresh"):
                self.full_url = r.content[r.content.find("URL=")+4:len(r.content)]
                self.full_url = self.full_url[0:self.full_url.find('"')]
            
            logger.debug('get_favicon_urls -> self.url = {0}'.format(self.url))
            logger.debug('get_favicon_urls -> self.full_url = {0}'.format(self.full_url))
            
            try:
                r = requests.get(self.full_url)
            except requests.exceptions.MissingSchema as e:
                print("Something went wrong! :( {0}".format(e))
                sys.exit()
        
            logger.debug('get_favicon_urls -> r = {0}'.format(r))
                    
            soup = BeautifulSoup(r.text.encode('utf-8'))
            try:
                icons = soup.head.find_all(rel="icon")
            except AttributeError as e:
                print("Error")
                
        self.favicon_url = [self.full_url + "/favicon.ico"]
        
        for icon in icons:
            logger.debug('get_favicon_urls -> icon[\'href\'] = {0}'.format(icon['href']))
            
            if (icon['href'].find("/") != 0):
                icon['href'] = "/" + icon['href']
            
            up = urlparse.urlparse(icon['href'])
            
            logger.debug('get_favicon_urls -> up = {0}'.format(up))
                
            if (up.scheme == ''):
                url_scheme = 'http'
            else:
                url_scheme = up.scheme
                
            if (up.netloc == ''):
                url_netloc = urlparse.urlparse(self.full_url).netloc
            else:
                url_netloc = up.netloc
                
            favicon = url_scheme + "://" + url_netloc + up.path
            
            logger.debug('get_favicon_urls -> favicon = {0}'.format(favicon))
            logger.debug('get_favicon_urls -> self.favicon_url = {}'.format(self.favicon_url))
            
            if (favicon not in self.favicon_url):
                self.favicon_url.append(favicon)
        
        logger.debug('get_favicon_urls -> self.favicon_url = {0}'.format(self.favicon_url))
    
    def save_favicon(self):
        if (os.path.exists(self.filename)):
            now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            self.filename = self.filename + "." + now + "." + self.get_favicon_type().lower()
        logger.debug('save_favicon -> self.filename = {0}'.format(self.filename))
        logger.info('save_favicon : Saving {0} ...'.format(self.filename))
        with open(self.filename,"wb") as f:
            f.write(self.icon)
    
    def get_favicon(self):
        METHOD_NAME = "get_favicon"
        if (len(self.favicon_url) > 0):
            rs = (frequests.get(url) for url in self.favicon_url)
            for r in frequests.map(rs):
                self.icon = r.content
                logger.debug('{} -> r.url = {}'.format(METHOD_NAME, r.url))
                t = r.url.split("/")
                up = urlparse.urlparse(self.full_url)
                
                logger.debug('get_favicon -> up = {0}'.format(up))
                
                if (t[len(t)-1] == 'favicon.ico' or t[len(t)-1] == 'favicon.png'):
                    self.filename = "favicon." + up.netloc + "." + self.get_favicon_type().lower()
                else:
                    self.filename = "favicon." + up.netloc + "-" + t[len(t)-1] + "." + self.get_favicon_type().lower()
                
                logger.debug('get_favicon -> self.filename = {0}'.format(self.filename))
                
                if self.is_valid_favicon():
                    self.save_favicon()
                else:
                    logger.info('get_favicon : Wrong icon!')
        else:
            logger.info('get_favicon : The page hasn''t got favicon!')

if __name__ == '__main__':
        
    DEBUG = False
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s -- %(levelname)s : %(name)s -- %(message)s')
    logger = logging.getLogger(__name__)

    logger.info('Start running script')
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('url', help='The URL of that page which has that nice favicon.')
    parser.add_argument('--debug', action="store_true", default=False, help='Switch on the debug mode.')
    parser.add_argument('--test', action="store_true", default=False, help='Switch on the test mode.')
    
    args = parser.parse_args()
    
    if args.debug:
        DEBUG = True
    
    if DEBUG:
        logger.setLevel(logging.DEBUG)
    
    if args.test:
        DEBUG = True
        logger.setLevel(logging.DEBUG)
        for p in test_pages:
            fd = FaviconDownloader(p)
            fd.get_favicon_urls()
            fd.get_favicon()
        
    fd = FaviconDownloader(args.url)
    fd.get_favicon_urls()
    fd.get_favicon()

    