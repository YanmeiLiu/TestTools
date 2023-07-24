# -*- coding: utf-8 -*-
import codecs
import csv
import json

# 适用于直接从服务器下载的日志，单独分析ip和dir
import time


def log_process(log_line, spider_dict):
    spider_dict["visits"] += 1

    log_line = json.loads(log_line)
    if ',' in log_line['http_x_forwarded_for']:
        spider_ip = log_line['http_x_forwarded_for'].split(',')[0]  # 获取蜘蛛ip,可能会存在多个ip，这里只取第一个
    else:
        spider_ip = log_line['http_x_forwarded_for']

    if spider_dict["visit_spider"].get(spider_ip):
        # 如果蜘蛛ip已经存在，那么就让它的访问次数加1
        spider_dict["visit_spider"][spider_ip] += 1
    else:
        # 如果是新的蜘蛛ip那么就创建，然后赋值为1
        spider_dict["visit_spider"][spider_ip] = 1

    url = log_line['request_uri']
    if spider_dict["visit_pages"].get(url):
        spider_dict["visit_pages"][url] += 1
    else:
        spider_dict["visit_pages"][url] = 1
    if url == '/':
        dirname = '/'
    elif url.count('/') >= 2:
        # 只获取一级目录
        dirname = '/%s/' % url.split('/')[1]
        # 获取完整目录使用：'/%s/' % '/'.join(url.split('/')[1: -1])
    else:
        dirname = ''

    if dirname and spider_dict["visit_dirs"].get(dirname):
        spider_dict["visit_dirs"][dirname] += 1
    elif dirname:
        spider_dict["visit_dirs"][dirname] = 1
    error_code = log_line['status']
    if error_code == '404':
        if spider_dict["error_pages"].get(url):
            spider_dict["error_pages"][url] += 1
        else:
            spider_dict["error_pages"][url] = 1


# 适用于直接从阿里云下载的csv日志
def aliyun_log_process(log_line, spider_dict):
    spider_dict["visits"] += 1
    #
    item = log_line.split('","')

    spider_ip = item[19]  # 获取蜘蛛ip
    # print("spider_ip:",spider_ip)
    if spider_dict["visit_spider"].get(spider_ip):
        # 如果蜘蛛ip已经存在，那么就让它的访问次数加1
        spider_dict["visit_spider"][spider_ip] += 1
    else:
        # 如果是新的蜘蛛ip那么就创建，然后赋值为1
        spider_dict["visit_spider"][spider_ip] = 1
    url = item[18]
    # print("url:",url)
    if spider_dict["visit_pages"].get(url):
        spider_dict["visit_pages"][url] += 1
    else:
        spider_dict["visit_pages"][url] = 1

    if url == '/':
        dirname = '/'
    elif url.count('/') >= 2:
        # 只获取一级目录
        dirname = '/%s/' % url.split('/')[1]
        # 获取完整目录使用：'/%s/' % '/'.join(url.split('/')[1: -1])
    else:
        dirname = ''
    if dirname and spider_dict["visit_dirs"].get(dirname):
        spider_dict["visit_dirs"][dirname] += 1
    elif dirname:
        spider_dict["visit_dirs"][dirname] = 1
    error_code = item[13]
    # print(error_code)
    if error_code == '404':
        if spider_dict["error_pages"].get(url):
            spider_dict["error_pages"][url] += 1
        else:
            spider_dict["error_pages"][url] = 1


# 单独分析ip和dir
def count_and_save(spider_dict, writer, reverse=True):
    # 对统计结果字典进行排序
    sort_spider = sorted(spider_dict["visit_spider"].items(), key=lambda x: x[1], reverse=reverse)
    sort_pages = sorted(spider_dict["visit_pages"].items(), key=lambda x: x[1], reverse=reverse)
    sort_dirs = sorted(spider_dict["visit_dirs"].items(), key=lambda x: x[1], reverse=reverse)
    sort_error = sorted(spider_dict["error_pages"].items(), key=lambda x: x[1], reverse=reverse)
    # print(len(sort_dirs))

    # 将结果写入文件
    fields = ("总访问量", "蜘蛛ip", "ip访问次数", "受访目录", "目录访问次数",
              "受访页面", "页面访问次数", "错误页面", "出错次数")
    writer.writerow(fields)  # writerow方法可以将列表或元组中的每个元组写入到一行，每个元素占一列
    row_list = ['' for _ in range(9)]  # 单独的下划线表示一个占位变量，不需要用到它
    # sp_len = len(sort_pages)
    # 作业：用for i in range(sp_len):实现
    # 将上面4项中长度最大的取出来
    len_max = max([len(sort_spider), len(sort_pages), len(sort_dirs), len(sort_error)])
    # print('循环次数是:', len_max)
    for i in range(0, len_max):
        row_list[0] = spider_dict["visits"] if i == 0 else ''

        ss = sort_spider.pop(0) if sort_spider else ''
        sd = sort_dirs.pop(0) if sort_dirs else ''
        sp = sort_pages.pop(0) if sort_pages else ''
        sr = sort_error.pop(0) if sort_error else ''

        """
        if sort_spider:
            ss = sort_spider.pop(0)
        else:
            ss = ''
        """
        if i == 0:
            row_list[1] = '本次访问的ip个数'
            row_list[2] = len(sort_spider)
            row_list[3] = '本次访问的目录个数'
            row_list[4] = len(sort_dirs)
            row_list[5] = '本次访问的页面个数'
            row_list[6] = len(sort_pages)
            row_list[7] = '本次访问出错的页面个数'
            row_list[8] = len(sort_error)

        else:

            row_list[1] = ss[0] if ss else ''
            row_list[2] = ss[1] if ss else ''
            row_list[3] = sd[0] if sd else ''
            row_list[4] = sd[1] if sd else ''

            row_list[5] = sp[0] if sp else ''
            row_list[6] = sp[1] if sp else ''

            row_list[7] = sr[0] if sr else ''
            row_list[8] = sr[1] if sr else ''

        writer.writerow(row_list)


def make_spider(spider_name):
    now_time = time.localtime()
    dt = time.strftime('%Y%m%d%H%M%S', now_time)
    file_name = str(spider_name) + '_' + dt

    save_file = open("../../results_file/spider/%s.csv" % file_name, "w", newline='\n',
                     encoding='utf-8')  # w模式在windows下写入csv的时候会多出一个空行，所以要用wb模式就可以忽略
    save_file.write(codecs.BOM_UTF8.decode('utf-8'))  # 在文件一开始就写入一个utf8的bom头，处理Excel utf-8中文乱码问题
    csvwriter = csv.writer(save_file)

    # 创建字典
    spider_name = dict()
    spider_name["visits"] = 0  # 统计总访问量
    spider_name["visit_spider"] = {}  # 蜘蛛ip统计
    spider_name["visit_pages"] = {}  # 访问页面统计
    spider_name["visit_dirs"] = {}  # 访问目录统计
    spider_name["error_pages"] = {}  # 错误页面统计
    return spider_name, csvwriter, save_file
