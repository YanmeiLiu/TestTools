#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import logging
import os


def write_log(name):
    logger = logging.getLogger(name)
    logger.setLevel(level=logging.INFO)
    # 获取当前时间
    dt = datetime.datetime.now().strftime('%Y%m%d')
    # 按照事件设置日志名称
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), name+'_' + dt + '.log')
    handler = logging.FileHandler(filename)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def res_log():
    filename = os.path.dirname(os.path.abspath(__file__)) + '/res.txt'
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - [%(pathname)s] - [line:%(lineno)d] - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[logging.FileHandler(encoding='utf-8', mode='a', filename=filename)]
                        )
    return logging


if __name__ == '__main__':
    write_log = write_log(__name__)
