# -*- coding: utf-8 -*-

import sys
import re
from urllib.parse import urlparse
from urllib.request import urlopen


class Main():

    """
    """

    def __init__(self):
        self.FILTER_WORDS = {'': ""}
        self.ILLEGAL_CHARS_PATN = r'[;]'
        self.StoreSiteNameAndRepl = {}    # this stores sitename and its replacement that we used
        self.startWebPage = ""
        self.enteredUrl = ""
        self.fixedUrl = ""  # from fix
        self.commonPath = "" # contains the option folder name eg. 'php/intermediate'
        self.commonName = ""  # / becomes index.html  and the like
        self.passedUrl = ""  # from protocol, This is the one that gets crawled

        # Data
        self.downloadedStringData = ""
        self.downloadedBytesData = b""

        # Parse Data
        self.newlyFoundUrls = []
        self.toCrawlUrls = []
        self.crawledUrls = []

        # Replacement Data
        self.replacedDownloadedStringData = ""

    def prepare(self, web_page_link):
        # More like the __init__ func
        # just this one is exposed

        # Set variable
        self.startWebPage = web_page_link

        # call the start
        self.start(self.startWebPage)

    def start(self, web_address):
        # Calls all the process

        # get address
        if self.get_address(web_address):
            pass
        else:
            print('get_address: err')
            return False

        # fix add
        if self._fix_url():
            pass
        else:
            print('_fix_url: err')
            return False
        
        # protocol
        self._check_protocol(self.fixedUrl)

        # check common name
        self._store_common_name(self.passedUrl)

        # Download
        data = self._download_data(self.passedUrl)
        # check if html, css or image mainly string or bytes
        dt = self._check_type_of_data(data)
        if dt['type'] == 'string':
            self._store_str_data(data)
            if dt['name'] is 'html':
                self._parser(data)
                self._gather_links(data)
                self.replacedDownloadedStringData = self._replace_data(data=data)
                self._save_data_offline(self.replacedDownloadedStringData)
        else:
            self._store_bytes_data(data)

    def get_address(self, webpage_addr):
        # split to avoid the url duplication in some urls
        raw_addr = [n for n in re.split(r'https://|http://', webpage_addr) if n != ''][0]
        # remove unacceptable characters
        nn = re.findall(self.ILLEGAL_CHARS_PATN, raw_addr)
        # TODO
        # Try url decoding
        if nn:
            print('Error. This is not a valid Url')
            return False

        # set the working address
        self.enteredUrl = raw_addr

        return True

    def _fix_url(self):
        # fix the url before we can continue
        # append only http for now
        if '://' not in self.enteredUrl:
            self.fixedUrl = 'http://' + self.enteredUrl
        else:
            self.fixedUrl = self.enteredUrl

        return True

    def _store_common_name(self, addr):
        parsed = urlparse(addr)
        path = parsed.path
        self.commonName = addr
        return True

    def _check_protocol(self, web_addr):
        # check the protocol of the address
        if 'ftp://' in web_addr:
            protocol = 'ftp'
        elif web_addr.startswith(('http://', 'https://')):
            protocol = 'http'

        self.passedUrl = web_addr
        return protocol

    def _download_data(self, link):
        # pass
        data = b''
        return data

    def _check_type_of_data(self, data):
        # pass
        dt = {'type': "", 'name': ""}
        return dt

    def _store_str_data(self, data):
        # pass
        pass

    def _store_bytes_data(self, data):
        # pass
        pass

    def _parser(self, data):
        # pass
        pass

    def _gather_links(self, data):
        # pass
        pass

    def _replace_data(self, key=None, data=None):
        return data

    def _save_data_offline(self, data):
        # pass
        pass

    def _check_for_more_urls(self):
        # pass
        pass

    def _clear(self):
        # pass
        pass

    def _repeat_process(self):
        # pass
        pass

main = Main()
main.prepare("https://www.w3schools.com/html/default.asp/http://")
