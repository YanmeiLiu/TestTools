#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 该模块的功能是： 快速生成神策的sql查询语句
# date :2021-5-28
# author: liuyanmei
import math
import time
import pandas as pd

# 查询今天的数据
from config.setconfig import get_dir
from tools.opt_file.optFiles import ReadFileAsDF, ConversionBigNum


def SelectByDate(date=time.strftime("%Y-%m-%d", time.localtime())):
    default_items = " select distinct_id,userid,time,event,filename,filevalue,kindvalue,$url_path,userlogin,page_name,mp,channel " \
                    "from events where date='%s' order by time desc;" % (
                        date)
    print(default_items)


# 默认查询今天某一用户的数据

def SelectByUser(distinct_id, date=time.strftime("%Y-%m-%d", time.localtime())):
    default_items = " select time,event,filename,filevalue,kindvalue,$url_path,userlogin,userid,page_name,mp,channel " \
                    "from events where date='%s' and distinct_id ='%s' order by time desc;" % (
                        date, distinct_id)
    print(default_items)


# 默认查询今天某一事件的数据

def SelectByEvent(event, date=time.strftime("%Y-%m-%d", time.localtime())):
    default_items = " select user_id,userid,time,event,filename,filevalue,kindvalue,$url_path,userlogin,page_name,mp,channel " \
                    "from events where date='%s' and event='%s' order by time desc;" % (
                        date, event)
    print(default_items)


def SelectByDistinctID(df, start_at=None, end_at=None,
                       date=time.strftime("%Y-%m-%d", time.localtime())):
    default_ = "select userid,time,$os,$browser,event,$is_first_day,$is_first_time,$url_host," \
               "$latest_traffic_source_type,fromsource,$referrer_host,$referrer,filename,filevalue,$url_path," \
               "$url,page_name,mp,channel,$url from events where "
    # 判断df
    if isinstance(df, pd.DataFrame):
        sql_lists = []
        if start_at is None and end_at is None:
            for i in df[df.result == 'yes']['user_id_1']:
                sql_ = " user_id  = %s and date='%s' " % (i[1:], date)
                sql_complete = default_ + sql_ + 'order by time ;'
                sql_lists.append(sql_complete)
        elif start_at is not None and end_at is not None:
            # print(df[df.result=='no'])

            for i in df[df.result == 'no']['user_id_1']:
                sql_ = " user_id =%s and date>='%s'  and date<='%s'" % (i[1:], start_at, end_at)
                sql_complete = default_ + sql_ + 'order by time ;'
                sql_lists.append(sql_complete)
        elif start_at is None and end_at is not None:
            for i in df['user_id_1']:
                sql_ = " user_id =%s and  date<='%s'" % (i[1:], end_at)
                sql_complete = default_ + sql_ + 'order by time ;'
                sql_lists.append(sql_complete)
        elif start_at is not None and end_at is None:
            for i in df['new_id']:
                sql_ = " user_id =%s and date>='%s' " % (i[1:], start_at)
                sql_complete = default_ + sql_ + 'order by time ;'
                sql_lists.append(sql_complete)
        else:
            sql_complete = default_[:-4]
            sql_lists.append(sql_complete)
        #     打印出sql_lists，判断字符串长度
        if len(sql_lists) < 100:
            for sql in sql_lists:
                truncateStr(sql, 100)

        else:
            sql_lists_count = math.ceil(len(sql_lists) / 100)
            for slc in range(0, sql_lists_count):
                print('\n')
                print('第{}部分数据'.format(slc + 1), '#' * 100)
                for sql in sql_lists[slc * 100:(slc + 1) * 100]:
                    # print(sql)
                    truncateStr(sql, 100)
    else:
        print('df在SelectByDistinctID错误')


# 将字符串截断换行显示

def truncateStr(strs, line_nums=100):
    """
    :param str:
    :param line_nums: 每行显示字数
    :return:
    """
    if len(strs) < line_nums:
        return strs
    else:
        count = math.ceil(len(strs) / line_nums)
        start_num = 0
        for c in range(0, count):
            # 末尾字符串是空格，逗号等可以换行，如果不是则+1直到是空格或者逗号
            tail_num = (c + 1) * line_nums
            while tail_num < len(strs):
                if strs[tail_num] == '' or strs[tail_num] == ',' or strs[tail_num] == ';':
                    print(strs[start_num:tail_num + 1], '\t')
                    # 将最后一个值赋予start_num
                    break
                elif tail_num == len(strs):
                    print(strs[start_num:], '\t')
                    print('\n')
                else:
                    tail_num = tail_num + 1
            start_num = tail_num + 1


def SelectGroupByDistinctID(file_name, start_at=None, end_at=None, start_num=None, end_num=None,
                            date=time.strftime("%Y-%m-%d", time.localtime())):
    df = ReadFileAsDF(file_name, sheet_name='Sheet1')
    str_distinct_id = ''
    for i in df['new_神策 ID'][start_num:end_num]:
        # print(i)
        str_distinct_id = str_distinct_id + "," + str(i[1:])

    #     将头部的，改成（，尾部加 ）
    new_string = str_distinct_id[:0] + "(" + str_distinct_id[0 + 1:]
    new_string = new_string + ")"
    if start_at is None and end_at is None:
        default_items = "select distinct_id,count(1) from events " \
                        "where  distinct_id in %s and date='%s' group by distinct_id ;" % (new_string, date)
        # print(default_items)
    elif start_at is not None and end_at is not None:
        # default_items = "select distinct_id,count(1) from events " \
        #                 "where date>='%s' and date<='%s' " \
        #                 "and event='WebClick' and filename not in %s and distinct_id in %s group by distinct_id ;" % (
        #                     start_at, end_at, ('Space_WriteComments', 'RateSelect_Select', 'Evaluation_WriteComments'),
        #                     new_string)
        # default_items = "select userid from events " \
        #                 "where date>='%s' and date<='%s' " \
        #                 "and distinct_id in %s ;" % (
        #                     start_at, end_at,
        #                     new_string)
        # 这个是留存的查询
        default_1 = "select date,time,event,user_id,userid,$is_first_day,$ip,$referrer_host,mp,channel,filename,filevalue,project_name,project_count,$url,$latest_traffic_source_type " \
                    "from events where  date>='%s' and date<='%s' and" \
                    " filename in ('Submit_Consult_Success'," \
                    "'Submit_Trial_Success'," \
                    "'Submit_Chat_UserInfo_Success'," \
                    "'Submit_Download_Success'," \
                    "'Submit_Pricing_Success'," \
                    "'Submit_UserInfo_Success'," \
                    "'Submit_Consult_Info_Success'," \
                    "'Submit_Price_Pricing_Success'," \
                    "'Submit_Discount_Success'," \
                    "'Submit_Contrast_UserInfo_Success') and user_id in %s order by time ;" % (
                        start_at, end_at, new_string)

        print(default_1[:173], '\n', default_1[173:339], '\n', default_1[339:521], '\n', default_1[521:])
        print('\t')
    elif start_at is None and end_at is not None:
        default_items = "select distinct_id,count(1) from events " \
                        "where  distinct_id in %s and date<='%s' group by distinct_id ;" % (
                            new_string, end_at)
        print(default_items)

    elif start_at is not None and end_at is None:
        default_1 = "select date,time,event,user_id,userid,$is_first_day,$ip,$referrer_host,mp,channel,filename,filevalue,project_name,project_count,$url,$latest_traffic_source_type " \
                    "from events where  date>='%s' and filename='VS_Detail' and user_id in %s ;" % (
                        start_at, new_string)
        print(default_1[:173], '\n', default_1[173:342], '\n', default_1[342:524], '\n', default_1[524:])
        print('\t')
    else:
        print('参数错误！')


# # 生成sql语句
# def getSQL(tbname,*args):
#     for i in args:
#         print(i)


if __name__ == '__main__':
    # SelectByDate()
    # SelectByUser(date='2021-6-15', distinct_id='179d46c68703b-0108e64b12614e-49183507-1296000-179d46c68715bb')
    # SelectByEvent(event='$pageview')
    filename = '20211207_061832.xlsx'  # 刚下载的用户行为列表
    file_name = get_dir('data_files/user_event', filename)
    df = ReadFileAsDF(file_name, sheet_name='sheet3')
    # new_df = ConversionBigNum(df, '神策 ID')

    SelectByDistinctID(df, '2021-11-30')
    # SelectByDistinctID(file_name, '2021-10-14', '2021-10-14')
