#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import time
import os
import configparser

# 封装返回路径的方法
from selenium import webdriver


def BaseDir():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return base_dir


def get_dir(folder_name, file_name):
    base_dir = BaseDir()
    file_dir = os.path.join(base_dir, folder_name, file_name)

    return file_dir


class Config:
    # 添加chrome user_agent
    options = webdriver.ChromeOptions()
    options.add_argument('lang=zh_CN.UTF-8')
    options.add_argument("ignore-certificate-errors")

    options.add_argument(
        'user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"')
    # 以时间生成保存文件名
    name = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    function_name = sys._getframe().f_code.co_name
    # INDEX_URL = "https://m.qsebao.com/"
    SCREEN_SHOOTPATH = "./screen_shoot/" + name + ".png"
    REPORT_PATH = BaseDir() + "/report/" + function_name + ".html"
    # PRO_REPORT_PATH = "/var/www/BigHealth/static/report/" + name + ".html"
    SCREEN_WIDTH = 375
    SCREEN_HEIGHT = 812
    CHROME_USER_AGENT = options


def shoot_file_name(case_name):
    screen_path = os.path.split(os.path.realpath(__file__))[0]

    return screen_path + '/screen_shoot/' + case_name + '-' + time.strftime('%Y%m%d%H%M%S',
                                                                            time.localtime(time.time())) + '.png'


def shoot_file_name(case_name):
    screen_path = os.path.split(os.path.realpath(__file__))[0]

    return screen_path + '/screen_shoot/' + case_name + '-' + time.strftime('%Y%m%d%H%M%S',
                                                                            time.localtime(time.time())) + '.png'




# 重写读取配置文件会更改大小写的方法，这里不会更改大小写
class myconf(configparser.ConfigParser):

    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=None)

    def optionxform(self, optionstr):
        return optionstr


if __name__ == '__main__':
    # print(shoot_file_name((sys._getframe().f_code.co_name)))
    file_path = get_dir(folder_name='data_files', file_name='case_base.xlsx')
