# -*- coding: utf-8 -*-

import sys
from urllib.request import urlopen


class Main():

    """
    """

    def __init__(self):
        self.FILTER_WORDS = {'': ""}
        self.startWebPage = ""
        self.enteredUrl = ""
        self.fixedUrl = ""  # from fix
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

    def get_address(self, webpage_addr):
        # set the working address

        self.enteredUrl = webpage_addr

        return True

    def _fix_url(self):
        # fix the url before we can continue

        return True

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

    def _replace_data(self, key, data):
        # pass
        pass

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
main.prepare("")
