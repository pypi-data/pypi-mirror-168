import os, re, sys, random, urllib.parse, json
from collections import defaultdict


def RM(patt, sr):
    mat = re.search(patt, sr, re.DOTALL | re.MULTILINE)
    return mat.group(1) if mat else ''

try: import requests
except: pass
def GetPage(url, cookie='', proxy='', timeout=5):
    try:
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
        if cookie != '': headers['cookie'] = cookie
        if proxy != '': 
            proxies = {'http': proxy, 'https': proxy}
            resp = requests.get(url, headers=headers, proxies=proxies, timeout=timeout)
        else: resp = requests.get(url, headers=headers, timeout=timeout)
        content = resp.content
        try: 
            import chardet
            charset = chardet.detect(content).get('encoding','utf-8')
            if charset.lower().startswith('gb'): charset = 'gbk'
            content = content.decode(charset, errors='replace')
        except:
            headc = content[:min([3000,len(content)])].decode(errors='ignore')
            charset = RM('charset="?([-a-zA-Z0-9]+)', headc)
            if charset == '': charset = 'utf-8'
            content = content.decode(charset, errors='replace')
    except Exception as e:
        print(e)
        content = ''
    return content

def GetJson(url, cookie='', proxy='', timeout=5.0):
    try:
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
        if cookie != '': headers['cookie'] = cookie
        if proxy != '': 
            proxies = {'http': proxy, 'https': proxy}
            resp = requests.get(url, headers=headers, proxies=proxies, timeout=timeout)
        else: resp = requests.get(url, headers=headers, timeout=timeout)
        return resp.json() 
    except Exception as e:
        print(e)
        content = {}
    return content

def FindAllHrefs(url, content=None, regex=''):
    ret = set()
    if content == None: content = GetPage(url)
    patt = re.compile('href="?([a-zA-Z0-9-_:/.%]+)')
    for xx in re.findall(patt, content):
        ret.add( urllib.parse.urljoin(url, xx) )
    if regex != '': ret = (x for x in ret if re.match(regex, x))
    return list(ret)

def Translate(txt):
    postdata = {'from': 'en', 'to': 'zh', 'transtype': 'realtime', 'query': txt}
    url = "http://fanyi.baidu.com/v2transapi"
    try:
        resp = requests.post(url, data=postdata, 
                       headers={'Referer': 'http://fanyi.baidu.com/'})
        ret = resp.json()
        ret = ret['trans_result']['data'][0]['dst']
    except Exception as e:
        print(e)
        ret = ''
    return ret
