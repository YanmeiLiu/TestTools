# coding:utf-8

import re
import csv
import requests


def getIndexFromChinaz(source_file, target_file):
    headers = ["关键词", "百度指数", "百度PC指数", "百度移动指数", "360指数", "神马指数"]
    with open(target_file, 'w') as fp:
        writer = csv.writer(fp)
        writer.writerow(headers)
        #     查询内容
        with open(source_file, encoding='utf-8') as kws:
            for line in kws:
                kw = line.strip()
                res = requests.post(url='http://rank.chinaz.com/ajaxsync.aspx?at=index&callback=',
                                    data={'kw': kw}, headers={'referer': 'http://rank.chinaz.com/wordsindex.aspx'})
                if res.status_code == 200:
                    tmp = re.findall(
                        "kw:'([\s\S]+)',index:'([0-9\-]+)',pcindex:'([0-9\-]+)',mindex:'([0-9\-]+)',index360:'([0-9\-]+)',indexsm:'([0-9\-]+)'",
                        res.text)
                    print(tmp)
                    if len(tmp) > 0:
                        writer.writerow(list(tmp[0]))
                    else:
                        writer.writerow([kws, 'None', 'None', 'None', 'None', 'None'])
                else:
                    print(res)


if __name__ == '__main__':
    getIndexFromChinaz('kw.txt', 'indexs.csv')
