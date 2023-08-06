#!/home/ai-046/anaconda3/bin/python3
# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# @File Name:        utils.py
# @Author:           wen
# @Version:          ver0_1
# @Created:          2022/2/10 上午10:56
# @Description:      Main Function:    xxx
# @Note:             xxx
# Function List:     hello() -- print helloworld
# History:
#       <author>    <version>   <time>      <desc>
#       wen         ver0_1      2020/12/15  xxx
# ------------------------------------------------------------------

import requests
import hashlib
import random
import time

class Translator:
    def __init__(self):
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'

        self.headers = {
            'Cookie': 'OUTFOX_SEARCH_USER_ID=-1927650476@223.97.13.65;',
            'Host': 'fanyi.youdao.com',
            'Origin': 'http://fanyi.youdao.com',
            'Referer': 'http://fanyi.youdao.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
        }
    def translate(self, content, from_str='AUTO', to_str='AUTO' ):
        '''
        可以进行多国语言翻译
        :param content: 要翻译的内容
        :param from_str: 要翻译的内容的语言, 默认auto
        :param to_str: 结果的语言, 默认auto
        :return:
        '''
        r = str(round(time.time() * 1000))
        salt = r + str(random.randint(0, 9))

        # content = '你好'

        data = "fanyideskweb" + content + salt + "Tbh5E8=q6U3EXe+&L[4c@"
        sign = hashlib.md5()

        sign.update(data.encode("utf-8"))

        sign = sign.hexdigest()
        data = {
            'i': str(content),
            'from': from_str,
            'to': to_str,
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': str(salt),
            'sign': str(sign),
            # 'lts': '1612879546052',
            # 'bv': '6a1ac4a5cc37a3de2c535a36eda9e149',
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_REALTlME',
        }
        res = requests.post(url=self.url, headers=self.headers, data=data).json()
        return res['translateResult'][0][0]['tgt']

def translate(s: str, sleeptime=None):
    '''
    只能进行中英翻译
    :param s:
    :param sleeptime:
    :return:
    '''
    url = "http://fanyi.youdao.com/translate"
    data = {
        'doctype': 'json',
        'type': 'AUTO',
        'i': s
    }
    r = requests.get(url, params=data)
    result = r.json()
    if sleeptime: time.sleep(sleeptime)
    return result['translateResult'][0][0]['tgt']
