# -*- coding: gbk -*-
# ==========================================================================
#   Copyright (C) 2015-2020 All rights reserved.
#
#   filename : CDRetainer.py
#   author   : chendian / okcd00@qq.com
#   date     : 2015-11-10
#   desc     : Retainer for ipv4 proxy pool.
#   All resources from network, this project is only used for study and research.
# ==========================================================================
from utils import *


def test_vars():
    print(valid_dumps, valid_url_case)


def extract_from_xici():
    url_case = [
        "http://www.xicidaili.com/nn/", "http://www.xicidaili.com/nt/",
        "http://www.xicidaili.com/wn/", "http://www.xicidaili.com/wt/"]
    ret_list = []
    for _idx, url in enumerate(url_case):
        doc = get_doc(url)
        soup = get_soup(doc)
        for table in soup.find_all('table'):
            if table.find('tr'):
                for tr in table.find_all('tr'):
                    if tr.find('td'):
                        # changed @ 2020-02-12
                        _ip = tr.find_all('td')[1].get_text()
                        _port = tr.find_all('td')[2].get_text()
                        _proxy = _ip.strip() + ":" + _port.strip()
                        ret_list.append(_proxy)
    return ret_list


def extract_from_nima():
    url_case = [
        'http://www.nimadaili.com/gaoni/',
        'http://www.nimadaili.com/http/',
        'http://www.nimadaili.com/https/']
    ret_list = []
    for _idx, url in enumerate(url_case):
        doc = get_doc(url)
        soup = get_soup(doc)
        for t_body in soup.find_all('tbody'):
            if t_body.find('tr'):
                for tr in t_body.find_all('tr'):
                    if tr.find('td'):
                        _proxy = tr.find_all('td')[0].get_text()
                        # _ip, _port = _proxy.strip().split(':')
                        ret_list.append(_proxy)
    return ret_list


def start_extraction():
    # test_Vars()
    proxy_list = []
    target_list = [
        (extract_from_xici, 'XICI'),  # www.xicidaili.com
        (extract_from_nima, 'NIMA'),  # www.nimadaili.com
    ]

    for (extract_fn, name) in target_list:
        try:
            results = extract_fn()
            proxy_list.extend(results)
            l.Notice("{} Finished with {} results.".format(name, results.__len__()))
        except Exception as ex:
            l.Warning("{} Failed for {}".format(name, str(ex)))

    cnt = {}
    length_t, length_p = len(valid_url_case), len(proxy_list)
    for idx in range(0, length_t):
        cnt[idx] = 0
    for each in proxy_list:
        tmp = each.split(':')
        ip, port = tmp[0], tmp[1]
        for idx in range(0, length_t):
            if test_proxy(ip, port, idx):
                cnt[idx] += 1
    l.Notice("Crawl Finished, Result Below:")
    for idx in range(0, length_t):
        rest_count = length_p
        l.Notice("[Target {}] ({}/{}) Passed {}\n".format(
            str(idx), str(cnt[idx]), str(rest_count), valid_url_case[idx]))


def start_cleaning():
    for idx, (file_name, test_url) in enumerate(zip(valid_dumps, valid_url_case)):
        print("Now cleaning on {}".format(file_name))
        file_path = os.path.join('.', 'data', file_name)
        shutil.copy(file_path, file_path+'.bak')  # backup
        pass_list = []
        proxy_list = [line.strip() for line in open(file_path.format(file_name), 'r')]
        proxy_list = list(set(proxy_list))
        with open(file_path, 'w') as f:
            for ip, port in [px.split(':') for px in proxy_list]:
                if test_proxy(ip, port, idx):
                    current_addr = '{}:{}\n'.format(ip, port)
                    pass_list.append(current_addr)
                    f.write(current_addr)
            print("Now write results back into {}".format(file_path))
        if [line for line in open(file_path, 'r')].__len__() <= 1:
            shutil.copy(file_path + '.bak', file_path)  # safe control
    return True


if __name__ == '__main__':
    # start_extraction()
    start_cleaning()

