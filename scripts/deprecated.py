from ..utils import *


def extract_from_cz88():
    url = "http://www.cz88.net/proxy/"
    doc = get_doc(url)
    soup = get_soup(doc)
    ret_list = []
    for d in soup.find_all('div') :
        if d.get('id') and d['id'] == 'boxright':
            flag = True
            for li in d.find_all('li'):
                if flag:
                    flag = False
                    continue
                else:
                    ip = li.find_all('div')[0].get_text().strip()
                    port = li.find_all('div')[1].get_text().strip()
                    pxy = ip.strip() + ":" + port.strip()
                    ret_list.append(pxy)
    return ret_list


def extract_from_p360():
    url = "http://www.proxy360.cn/Proxy"
    doc = get_doc(url)
    soup = get_soup(doc)
    ret_list = []
    for table in soup.find_all('table'):
        for div in table.find_all('div', 'proxylistitem'):
            if div.find('span'):
                ip = div.find_all('span')[0].get_text()
                port = div.find_all('span')[1].get_text()
                pxy = ip.strip() + ":" + port.strip()
                ret_list.append(pxy)
    return ret_list


def extract_from_kuai():
    url_head = "http://www.kuaidaili.com/proxylist/pagesites/"
    ret_list = []
    for idx in range(1, 11):
        url = url_head.replace('pagesites',str(idx))
        doc = get_doc(url)
        soup = get_soup(doc)
        for table in soup.find_all('table') :
            if table.find('tr') :
                for tr in table.find_all('tr') :
                    if tr.find('td'):
                        ip = tr.find_all('td')[0].get_text()
                        port = tr.find_all('td')[1].get_text()
                        pxy = ip.strip() + ":" + port.strip()
                        ret_list.append(pxy)
    return ret_list


if __name__ == '__main__':
    print("pass")
