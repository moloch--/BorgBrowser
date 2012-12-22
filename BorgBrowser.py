# -*- coding: utf-8 -*-
'''
Created on Dec 22, 2012

@author: moloch

A browser-like Python class that can be configured to automatically change
user agent, and proxy.  Automatically parses HTML and JSON responses and exposes
Python objects for easy manipulation and data extraction.  Resistance is futile.

----------------------------------------------------------------------------------
    Copyright 2012

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
----------------------------------------------------------------------------------
'''

import time
import json
import requests

from random import choice
from BeautifulSoup import BeautifulSoup


USER_AGENTS = [
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)",
    "Opera/9.20 (Windows NT 6.0; U; en)",
    "Opera/9.00 (Windows NT 5.1; U; en)",
    "Googlebot/2.1 ( http://www.googlebot.com/bot.html)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.95 Safari/537.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:17.0) Gecko/20100101 Firefox/17.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11",
    "Mozilla/5.0 (Linux; U; Android 2.2; fr-fr; Desire_A8181 Build/FRF91)",
]

class BorgBrowser(object):
    ''' Main browser class '''

    def __init__(self):
        self.history = []
        self.cookies = {}
        self.cert_validation = False
        self.follow_redirects = True
        self.random_proxy = False
        self.__response__ = None
        self.__proxies__ = []
        self.proxy_traffic = False

    def set_proxies(self, proxies):
        if isinstance(proxies, basestring):
            proxies = [proxies]
        self.proxy_traffic = True
        self.__proxies__ = proxies

    @property
    def proxy(self):
        _proxy = choice(self.__proxies__)
        return {'http': _proxy, 'https': _proxy}

    @property
    def user_agent(self):
        return choice(USER_AGENTS)

    @property
    def page(self):
        if self.__response__.status_code == requests.codes.ok:
            return BeautifulSoup(self.__response__.text)
        else:
            return None

    def get(self, uri, **parameters):
        self.history.append(uri)
        self.__response__ = requests.get(
            uri, 
            cookies=self.cookies, 
            params=parameters, 
            verify=self.cert_validation
        )
        return self.__response__

    def post(self, uri, **parameters):
        self.history.append(uri)
        self.__response__ = requests.post(uri, cookies=self.cookies, params=parameters, verify=self.cert_validation)
        return self.__response__

    def put(self, uri, **parameters):
        self.history.append(uri)
        self.__response__ = requests.post(uri, cookies=self.cookies, params=parameters, verify=self.cert_validation)
        return self.__response__

    def delete(self, uri, **parameters):
        self.history.append(uri)
        self.__response__ = requests.post(uri, cookies=self.cookies, params=parameters, verify=self.cert_validation)
        return self.__response__

    def head(self, uri, **parameters):
        self.history.append(uri)
        self.__response__ = requests.post(
            uri, 
            cookies=self.cookies, 
            params=parameters, 
            verify=self.cert_validation
        )
        return self.__response__

    def options(self, uri, **parameters):
        self.history.append(uri)
        self.__response__ = requests.post(uri, cookies=self.cookies, params=parameters, verify=self.cert_validation)
        return self.__response__
