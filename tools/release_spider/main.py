# -*- coding: utf-8 -*-

# 百度蜘蛛
import re

from TestTools.config.setconfig import get_dir
from TestTools.tools.release_spider.check_charset import check_charset
from TestTools.tools.release_spider.logAnalysis import make_spider, log_process, count_and_save

"""
*搜索引擎爬虫名称：
    百度（Baiduspider）
    搜狗（sogou spider）
    神马（YisouSpider）
    谷歌（Googlebot）
    360（360spider）
    必应（bingbot）
    头条（Bytespider）
    搜搜（Sosospider）
    雅虎（Yahoo! Slurp）
"""
baidu, baiducsv, baidufile = make_spider("baidu")
# 搜狗蜘蛛
sougou, sougoucsv, sougoufile = make_spider("sougou")
# 神马蜘蛛 对应神策里面爬虫姓名是 ：Geneic Bot
shenma, shenmacsv, shenmafile = make_spider("shenma")
# 谷歌蜘蛛
google, googlecsv, googlefile = make_spider("google")
# 360蜘蛛
spider_360, spider_360csv, spider_360file = make_spider("spider_360")
# 必应蜘蛛
bingbot, bingbotcsv, bingbotfile = make_spider("Bingbot")
# 头条蜘蛛
bytespider, Bytespidercsv, Bytespiderfile = make_spider("Bytespider")
# 搜搜蜘蛛
sosospider, sosocsv, sosofile = make_spider("Sosospider")
# 搜搜蜘蛛
Yahoo, Yahoocsv, Yahoofile = make_spider("Yahoospider")

# Lighthouse, Lighthousecsv, Lighthousefile = make_spider('Lighthouse')
# WordPress, WordPresscsv, WordPressfile = make_spider('WordPress')
file_path = get_dir('data_files/user_events', 'downloaded_bing_data.txt')
with open(file_path, 'r', encoding=check_charset(file_path)) as logfile:
    print("开始分析日志")
    # # 读取文件内容
    # temp = logfile.read()
    # # 将文件按行数分成列表
    # line_list = temp.splitlines()
    # # 声明变量储存列表长度
    # lines = len(line_list)
    count = 0
    spider_baidu_regex = re.compile(r'baiduspider', re.I)
    spider_sougou_regex = re.compile(r'Sogou web spider', re.I)
    spider_shenma_regex = re.compile(r'YisouSpider', re.I)
    spider_google_regex = re.compile(r'Googlebot', re.I)
    spider_360_regex = re.compile(r'360spider', re.I)
    spider_bing_regex = re.compile(r'bingbot', re.I)
    spider_byte_regex = re.compile(r'Bytespider', re.I)
    spider_soso_regex = re.compile(r'Sosospider', re.I)
    spider_yahoo_regex = re.compile(r'Yahoo! Slurp', re.I)
    # spider_lighthouse_regex = re.compile(r'Lighthouse', re.I)
    # spider_WordPress_regex = re.compile(r'WordPress', re.I)

    for line in logfile:
        print(line)
        if spider_baidu_regex.search(line):
            log_process(line, baidu)
        elif spider_sougou_regex.search(line):
            log_process(line, sougou)
        elif spider_shenma_regex.search(line):
            log_process(line, shenma)
        elif spider_google_regex.search(line):
            log_process(line, google)
        elif spider_360_regex.search(line):
            log_process(line, spider_360)
        elif spider_bing_regex.search(line):
            log_process(line, bingbot)
        elif spider_byte_regex.search(line):
            log_process(line, bytespider)
        elif spider_soso_regex.search(line):
            log_process(line, sosospider)
        elif spider_yahoo_regex.search(line):
            log_process(line, Yahoo)
        # elif spider_lighthouse_regex.search(line):
        #     log_process(line, Lighthouse)
        # elif spider_WordPress_regex.search(line):
        #     log_process(line, WordPress)
        else:
            count += 1
            print(line)
    print(count)

    count_and_save(baidu, baiducsv)
    count_and_save(sougou, sougoucsv)
    count_and_save(shenma, shenmacsv)
    count_and_save(google, googlecsv)
    count_and_save(spider_360, spider_360csv)
    count_and_save(bingbot, bingbotcsv)
    count_and_save(bytespider, Bytespidercsv)
    count_and_save(sosospider, sosocsv)
    count_and_save(Yahoo, Yahoocsv)

    # count_and_save(Lighthouse, Lighthousecsv)
    # count_and_save(WordPress, WordPresscsv)

baidufile.close()
sougoufile.close()
shenmafile.close()
googlefile.close()
spider_360file.close()
bingbotfile.close()
Bytespiderfile.close()
sosofile.close()
Yahoofile.close()
# Lighthousefile.close()
# WordPressfile.close()

print("日志分析完毕")
