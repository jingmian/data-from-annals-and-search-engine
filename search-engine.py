import os
import csv
import urllib.parse
import requests
from lxml import etree
import time
import random

result_file = 'se_result.csv'
error_file = 'error_se_result.csv'
key_list = ['贸易摩擦', '贸易战', '出口', '境外', '美国', '进口']

file_list = os.listdir('pdf')

# csv文件头
csv_dic = {'证券代码': '', '证券简称': ''}
for key in key_list:
    csv_dic[key] = ''
with open(result_file, 'w') as f:  # Just use 'w' mode in 3.x
    w = csv.DictWriter(f, csv_dic.keys())
    w.writeheader()
with open(error_file, 'w') as f:  # Just use 'w' mode in 3.x
    w = csv.DictWriter(f, {'error_name': ''}.keys())
    w.writeheader()

index = 0
for file in file_list:

    # noinspection PyBroadException
    try:
        code_name = file.split('：')[0]
        code = code_name[:6]
        name = code_name[6:]
        print(file)
        print(code)
        print(name)
        dic = {'证券代码': code, '证券简称': name}
        for key in key_list:
            time.sleep((random.randint(1000, 5000) / 1000.0))
            url = 'http://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&word='
            word = urllib.parse.quote_plus(name) + '+' + urllib.parse.quote_plus(key)
            url = url + word
            headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ",
                       "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                       "Accept-Language": "en-us",
                       "Connection": "keep-alive",
                       "Accept-Charset": "GB2312,utf-8;q=0.7,*;q=0.7"}
            response = requests.get(url, headers=headers)
            num_str = etree.HTML(response.text).xpath('//span[@class="nums"]/text()')[0]
            num = num_str.replace('找到相关资讯', '').replace('约', '').replace('篇', '').replace(',', '')
            dic[key] = str(num)
            print(name + '   ' + key + '   ' + str(num))

        print(dic)
        with open(result_file, 'a') as f:
            w = csv.DictWriter(f, dic.keys())
            w.writerow(dic)
        index = index + 1
        print(str(index) + '   ' + str(len(file_list)))
        print(str(index) + '   ' + str(len(file_list)))
        print(str(index) + '   ' + str(len(file_list)))

    except Exception as e:
        print(e)
        sleep_sec = random.randint(300 * 1000, 600 * 1000) / 1000.0
        print('被反爬虫了，认输' + str(sleep_sec) + '秒')
        time.sleep(sleep_sec)
        error_file_dic = {'error_name': name}
        with open(error_file, 'a') as f:
            w = csv.DictWriter(f, error_file_dic.keys())
            w.writerow(error_file_dic)

print('FINISH')
print('FINISH')
print('FINISH')
print('FINISH')
print('FINISH')
print('FINISH')
