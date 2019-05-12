# -*- coding: utf-8 -*-

import sys
from urllib.request import urlopen

class Main():
    
    """
    """
    
    def __init__(self):
        self.startWebPage = "https://www.developers.com"
        self.enteredUrl = ""
        self.fixedUrl = ""  # from fix
        self.commonName = "" # / becomes index.html  and the like
        self.passedUrl = "" # from protocol # This is the one that will be crawled
        
        # Data
        self.downloadedStringData = ""
        self.downloadedBytesData = b""
        
        # Parse Data
        self.newlyFoundUrls = []
        self.toCrawlUrls = []
        self.crawledUrls = []
        
        # Replacement Data
        self.replacedDownloadedStringData = ""
    
    def get_addres(self, webpage_add):
        # pass
        pass
    
    def _fix_url(self, web_addr):
        # pass
        pass
    
    def _store_common_name(self, addr):
        # pass
        pass
    
    def _check_protocol(self, web_addr):
        # pass
        pass
    
    def _download_data(self, link):
        # pass
        pass
    
    def _check_type_of_data(self, data):
        # pass
        pass


Main()
