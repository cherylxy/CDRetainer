# -*- coding: gbk -*-
# ==========================================================================
#   Copyright (C) 2015-2020 All rights reserved.
#
#   filename : utils.py
#   author   : chendian / okcd00@qq.com
#   date     : 2015-11-10
#   desc     : packages and constants
# ==========================================================================

import os
import sys
import time
import random
import shutil
import logging

# from py2 to py3
import pickle as cPickle
from bs4 import BeautifulSoup
import urllib.request as urllib2
from multiprocessing import Pool
import configparser as ConfigParser

# constants and paths
from LogModule import LogModule
l = LogModule()
config = ConfigParser.ConfigParser()
config.read("./conf/basic.conf")
path_home = config.get("path", "path_home")
path_list = config.get("path", "path_list")
prx_switch = config.getint("para", "USE_PROXY")
exec_cyctime = config.getint("para", "EXEC_CYCLE_TIME")
wait_runtime = config.getint("para", "RUNTIME_WAITTIME")

proxy_cache = []
valid_dumps = [
    line.strip().split('@')[0].strip()
    for line in open(path_list, 'r')
    if not line.startswith('#')]
valid_url_case = [
    line.strip().split('@')[1].strip()
    for line in open(path_list, 'r')
    if not line.startswith('#')]
print('targets:', list(zip(valid_dumps, valid_url_case)))


def test_proxy(_ip, _port, target):
    try:
        time1 = time.time()
        proxy_handler = urllib2.ProxyHandler(
            {"http": '{}:{}'.format(_ip, _port)})
        opener = urllib2.build_opener(proxy_handler)
        urllib2.install_opener(opener)
        request = urllib2.Request(valid_url_case[target])
        request.add_header(
            'User-Agent', 'fake-client')
        response = urllib2.urlopen(
            request, timeout=wait_runtime)
        text = response.read()
        if len(text) > 10:
            time2 = time.time()
            if time2 - time1 < 10:
                fobj = open("{}/{}".format(str(path_home), valid_dumps[target]), "a")
                current_proxy = str(_ip) + ":" + str(_port)
                fobj.write('{}\n'.format(current_proxy))
                if prx_switch != 0 and len(proxy_cache) < 20 and not (current_proxy in proxy_cache):
                    proxy_cache.append(current_proxy)
                fobj.close()
                l.Notice("{}:{} Passed on [Target {}]".format(
                    str(_ip), str(_port), str(valid_dumps[target])))
                return True
        else:
            raise ValueError('Invalid response from {}'.format(text))
    except Exception as ex:
        l.Notice("{}:{} Failed, {}".format(
            str(_ip), str(_port), str(ex)))
        return False


def get_doc_with_proxy(url, pxy=None):
    if pxy is None:
        return get_doc_directly(url)
    _tmp = pxy.split(':')
    ip, port = _tmp[0], _tmp[1]
    proxy_handler = urllib2.ProxyHandler(
        {"http": '{}:{}'.format(ip, port)})
    opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener)
    request = urllib2.Request(url)
    request.add_header(
        'User-Agent', 'fake-client')
    html_doc = urllib2.urlopen(
        request, timeout=wait_runtime)
    return html_doc


def get_doc_directly(url):
    request = urllib2.Request(url)
    request.add_header('User-Agent', 'fake-client')
    html_doc = urllib2.urlopen(
        request, timeout=wait_runtime)
    return html_doc


def get_doc(url):
    if prx_switch == 0:
        doc = get_doc_directly(url)
        return doc
    else:
        try:
            doc = get_doc_directly(url)
            return doc
        except Exception as ex:
            l.Warning("Direct Crawl Failed at {} : {}\n".format(str(url), str(ex)))
            while len(proxy_cache) > 3:
                idx = random.randrange(0, len(proxy_cache), 1)
                current_proxy = proxy_cache[idx]
                l.Notice("{} Proxy_Crawling... ".format(str(current_proxy)))
                try:
                    doc = get_doc_with_proxy(url, current_proxy)
                    return doc
                except Exception as ex:
                    l.Warning("Proxy Crawl Failed at {}, Remove [{}] for {}".format(
                        str(url), str(current_proxy), str(ex)))
                    proxy_cache.remove(current_proxy)
                    continue
            return get_doc_directly(url)


def get_soup_html(html_doc, lang):
    readinto = html_doc.read()
    soup = BeautifulSoup(readinto.decode(lang), "html.parser")
    return soup


def get_soup(html_doc):
    readinto = html_doc.read()
    soup = BeautifulSoup(readinto, "lxml")
    return soup


if __name__ == '__main__':
    print("pass")
