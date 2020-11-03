# -*- coding: utf-8 -*-

import sys
import os
import re
from urllib.parse import urlparse
from urllib.request import urlopen

import chardet


class Main():

    """
    """

    def __init__(self):
        # Ezekiel
        self.store_folder = os.path.join(os.environ["USERPROFILE"], 'Ezekiel')
        self.domainFolder = ''

        self.FILTER_WORDS = {'': ""}
        self.ILLEGAL_CHARS_PATN = r'[;]'
        self.StoreSiteNameAndRepl = {}    # this stores sitename and its replacement that we used
        self.domain = ""
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
        self.htmlLinkPatt = ['href', 'src']
        self.cssLinkPatt = []
        # local
        self.newlyFoundUrls = []
        self.toCrawlUrls = []
        self.crawlingUrl = ''
        self.crawledUrls = []
        self.downloadedUrls = []
        # external
        self.newlyFoundExtUrls = []
        self.toCrawlExtUrls = []
        self.crawlingExtUrl = ''
        self.crawledExtUrls = []
        self.downloadedExtUrls = []

        # Replacement Data
        self.replacedDownloadedStringData = ""

        # Download
        # external
        self.allowedExtExt = ['.css', '.js', '.html', '.xhtml',
        '.xml', '.pdf', '.png', '.jpg', '.jpeg', '.gif']

    def prepare(self, web_page_link):
        print('Inside prepare\n')
        # More like the __init__ func
        # just this one is exposed

        # Set variable
        self.startWebPage = web_page_link

        # call the start
        self.start(self.startWebPage)

    def start(self, web_address):
        print('Inside start\n')
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

        # Download
        data = self._download_data(self.passedUrl)
        # Check if html, css or image. Basically string or bytes
        dt = self._check_type_of_data(data)
        if dt['type'] == 'string':
            self._store_str_data(data)
            if dt['name'] is 'html':
                self._parser(data)
                self._gather_links(data)
                self.replacedDownloadedStringData = self._replace_data(data=data)
                self._save_data_offline(self.replacedDownloadedStringData)
                self._handle_external(self.newlyFoundExtUrls)
                self._check_for_more_urls()
        else:
            self._store_bytes_data(data)

    def get_address(self, webpage_addr):
        print('Inside get_address\n')
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
        print('Inside _fix_url\n')
        # fix the url before we can continue
        # append only http for now
        if '://' not in self.enteredUrl:
            self.fixedUrl = 'http://' + self.enteredUrl
        else:
            self.fixedUrl = self.enteredUrl

        return True

    def _store_common_name(self, addr):
        print('Inside _store_common_name\n')
        cmnName = ''
        scheme, netloc, path, params, query, fragment = urlparse(addr)
        self.domain = netloc

        paths = path.rsplit('/', 1)
        if paths[-1] == '':
            cmnName = 'index.html'
        else:
            cmnName = paths[-1]

        self.commonName = cmnName
        self.commonPath = paths[0]
        self.crawlingUrl = self.commonPath + '/' + self.commonName
        return True

    def _check_protocol(self, web_addr):
        print('Inside _check_protocol\n')
        # check the protocol of the address
        if 'ftp://' in web_addr:
            protocol = 'ftp'
        elif web_addr.startswith(('http://', 'https://')):
            protocol = 'http'
        else:
            print('unknown protocol shoud raise an Exception')
            protocol = 'http'

        self.passedUrl = web_addr
        return protocol

    def _download_data(self, link):
        print('Inside _download_data\n')
        req = urlopen(link)

        # check common name
        self._store_common_name(req.geturl())

        data = req.read()
        return data

    def _download_ext_data(self, link):
        print('Inside _download_data\n')
        if not link.startswith('http'):
            link = 'http:' + link

        req = urlopen(link)

        data = req.read()
        return data

    def _check_type_of_data(self, data):
        print('Inside _check_type_of_data\n')
        dt = {'type': "", 'name': ""}
        
        # Using charder
        confidence = chardet.detect(data)['confidence']
        if confidence > 0.5:
            dt['type'] = 'string'

            if '<html' in str(data):
                dt['name'] = 'html'
            else:
                dt['name'] = 'css'

        else:
            dt['type'] = 'bytes'
        return dt

    def _store_str_data(self, data):
        print('Inside _store_str_data\n')
        # Rethink this function
        # might load memory
        # or even cause troubles
        # maybe with parser because its getting stored
        self.downloadedStringData = data

    def _store_bytes_data(self, data):
        print('Inside _store_bytes_data\n')
        # pass
        pass

    def _parser(self, data):
        print('Inside _parser\n')
        # The use of this function
        # may have been taken up by _gather_links
        pass

    def _gather_links(self, data):
        print('Inside _gather_links\n')
        # Gather links from either html or css
        # Still using data passed via parameter
        data = str(data)
        found_local = []
        found_ext = []
        for tag in self.htmlLinkPatt:
            patt = r'' + tag + r'\s*=\s*["|\'].*?.*?.*?["|\']'
            attr_links = re.findall(patt, data)
            all_links = [m.split('=', 1)[1].strip()[1:-1] \
                for m in attr_links]

            found_local.extend([n for n in all_links \
                if not n.startswith('http') \
                and not n.startswith('//') \
                and n not in self.crawledUrls \
                and n not in self.downloadedUrls])

            # add links to external
            for o in all_links:
                if o not in found_local \
                and o not in self.downloadedExtUrls:
                    _, _, path, _, _, _ = urlparse(o)
                    ext = os.path.splitext(path)[-1]
                    if ext in self.allowedExtExt:
                        found_ext.append(o)

        self.crawledUrls.append(self.crawlingUrl)
        self.newlyFoundUrls.extend(found_local)
        self.newlyFoundExtUrls.extend(found_ext)

    def _replace_data(self, key=None, data=None):
        print('Inside _replace_data\n')
        # because we are storing everything as they are
        # as if on the server this might be useful only for external

        # External is available only in the domain folder
        backpaths = '../' * (len(self.commonPath.split('/')) - 1)
        ext_folder = backpaths + '__external/'

        for link in self.newlyFoundExtUrls:
            new_link = ext_folder + link.split('//', 1)[-1]
            data = data.replace(
                bytes(link, 'utf-8'), bytes(new_link, 'utf-8'))

        return data

    def _save_data_offline(self, data):
        print('Inside _save_data_offline\n')
        self.domainFolder = os.path.realpath(os.path.join(
            self.store_folder,
            self.domain))
        folder_name = self.domainFolder + self.commonPath
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        path = os.path.join(folder_name, self.commonName)
        with open(path, 'wb') as online_file:
            online_file.write(data)
            self.downloadedUrls.append(self.crawlingUrl)

    def _save_ext_data_offline(self, data, link):
        # handle saving external file offline
        print('Inside _save_ext_data_offline')

        new_link = '__external/' + link.split('//', 1)[-1]
        path_name, cmnName = os.path.split(new_link)
        folder_name = os.path.join(self.domainFolder, path_name)
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        fileName = os.path.join(folder_name, cmnName)
        with open(fileName, 'wb') as ext_file:
            ext_file.write(data)

    def _check_for_more_urls(self):
        print('Inside _check_for_more_urls\n')
        # put all links if any in toCrawlUrls
        if self.newlyFoundUrls:
            self.toCrawlUrls.extend([u \
                for u in self.newlyFoundUrls \
                if u not in self.toCrawlUrls \
                if not u.startswith('#')])
            return True

    def _clear(self):
        print('Inside _clear\n')
        # pass
        pass

    def _handle_external(self, links):
        print('inside _handle_external')
        # carefully process links that are external
        for link in links:
            data = self._download_ext_data(link)
            self._save_ext_data_offline(data, link)

    def _repeat_process(self):
        print('Inside _repeat_process\n')
        # pass
        pass

main = Main()
#main.prepare("https://localhost/img/module_table_bottom.png")
main.prepare("https://localhost/")