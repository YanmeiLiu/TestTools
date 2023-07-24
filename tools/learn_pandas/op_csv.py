import pandas as pd
import numpy as np
from dateutil.parser import parse

from config.setconfig import get_dir

# 使用csv读取
base_name = 'query_result'
for i in range(54,55):
    if i == 0:
        csv_name = base_name + '.csv'
    else:
        csv_name = base_name + ' (' + str(i) + ').csv'
    print('处理', csv_name)
    file_name = get_dir('data_files/user_event', csv_name)
    df = pd.read_csv(file_name)
    # 新增两列 用于保存 计算结果
    col_name = df.columns.tolist()  # 将数据框的列名全部提取出来存放在列表里
    # col_name.insert(1, 'diff_time')  # 两个时间间隔，超过30min分钟的分割掉
    col_name.insert(2, 'url_no_list')  # 用于标记页面是否是连续的同一个页面
    # 新增一列数据用于保存页面的访问时长
    df.insert(1, 'diff_time', np.zeros(len(df)), allow_duplicates=True)
    df.insert(3, 'SumDiffTime', np.zeros(len(df)), allow_duplicates=True)

    # 处理时间差
    time_data = df['time']
    url_path = df['$url']
    total_sec = 0
    session_count = 1
    # 两个时刻的时间差
    diff_time = []
    for j in range(len(time_data)):
        if j >= 1:
            dee = (parse(time_data[j]) - parse(time_data[j - 1])).total_seconds()
            if dee <= 1800:
                df.loc[j, 'diff_time'] = dee
                total_sec += dee

            else:  # 时间大于30分钟就不要这段时间了
                df.loc[j, 'diff_time'] = 0
                session_count += 1
                total_sec = total_sec

        else:
            df.loc[j, 'diff_time'] = 0

    url_datas = df['$url']
    # 标记不同的url,为什么要多次一举 是因为用户访问过A页面后访问B页面再访问A页面，我们要统计三个页面的停留时长，要取连续一样的页面url
    # url不一样的是第几条数据，取出来
    diffrent_url_no = []  # 在哪个事件页面开始不一样
    url_no_list = []  # 页面标记列表
    url_no = 0  # 页面标记
    for m in range(len(url_datas)):
        if m > 0 and url_datas[m] == url_datas[m - 1]:  # 与上一条数据一样就继续
            # 新增一个字段赋值，url_no
            url_no = url_no
            url_no_list.append(url_no)
            continue
        elif m == 0:
            url_no = 0
            url_no_list.append(url_no)
            continue
        else:
            url_no += 1
            diffrent_url_no.append(m)
            url_no_list.append(url_no)
            continue
    df['url_no_list'] = url_no_list
    # print(diffrent_url_no)
    # 计算页面停留时长
    if len(diffrent_url_no) == 0:  # 只访问了一个页面
        print('只访问了一个页面')
        sum_data = df['diff_time'].sum()
        df.loc['总计', 'SumDiffTime'] = sum_data
    else:
        print('共访问了{}个页面'.format(len(diffrent_url_no) + 1))
        for z in range(len(diffrent_url_no) + 1):
            if z == 0:
                sum_data = df[1:diffrent_url_no[z] + 1]['diff_time'].sum()
                df.loc[diffrent_url_no[z], 'SumDiffTime'] = sum_data

            elif z == len(diffrent_url_no):
                sum_data = df[diffrent_url_no[z - 1] + 1:]['diff_time'].sum()
                df.loc['最后一个页面时长', 'SumDiffTime'] = sum_data
            else:

                sum_data = df[diffrent_url_no[z - 1] + 1:diffrent_url_no[z] + 1]['diff_time'].sum()
                df.loc[diffrent_url_no[z], 'SumDiffTime'] = sum_data
    df.loc['session次数', 'SumDiffTime'] = session_count
    df.loc['session时间总和', 'SumDiffTime'] = total_sec
    df.loc['session人均时长', 'SumDiffTime'] = total_sec / session_count

    # 替换文件中内容
    df['event'].replace(['$pageview', 'SubmitResult', '$WebClick', 'WebClick', '$WebStay', 'PopupTrack', 'ModuleView'],
                        ['访问页面', '提交数据结果', '全埋点事件的Web元素点击', '手动埋点击事件', 'Web 视区停留', '弹窗事件', '模块露出'], inplace=True)
    df['$is_first_day'].replace([1, 0], ['是', '否'], inplace=True)
    df['$is_first_time'].replace([1, 0], ['是', '否'], inplace=True)

    # 替换文件头
    df = df.rename(
        columns={'time': '访问时间', 'event': '事件类型', '$is_first_day': '是否首日访问', '$is_first_time': '是否首次触发事件',
                 '$latest_traffic_source_type': '流量来源类型', '$referrer_host': '前向域名', 'filename': '事件名称',
                 'filevalue': '事件值', '$url': '页面地址', 'page_name': '页面名称', 'diff_time': '时间差', 'SumDiffTime': '页面访问时长',
                 'url_no_list': '页面标记'})
    # 输出文件
    xlsx_name = get_dir('data_files', 'users1.xlsx')
    with pd.ExcelWriter(xlsx_name, mode='a', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='sheet' + str(i), index=True)
