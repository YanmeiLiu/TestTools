import datetime
from dateutil.parser import parse
import numpy as np
import pandas as pd

# 使用csv读取
from config.setconfig import get_dir

file_name = get_dir('data_files', 'query_result (54).csv')
df = pd.read_csv(file_name)

# 增加几列数据,方式一

# 用于存放每个页面的访问时长
df.insert(len(df.columns), 'SumDiffTime', np.zeros(len(df)), allow_duplicates=True)
# 增加几列数据，方式二
col_name = df.columns.tolist()  # 将数据框的列名全部提取出来存放在列表里
col_name.insert(1, 'diff_time')
col_name.insert(2, 'url_no_list')

# print(df.head(14))
time_data = df['time']
url_path = df['$url']
# print(time_data)
total_sec = 0
session_count = 1
# 两个时刻的时间差
diff_time = []
# print(len(time_data))
for j in range(len(time_data)):
    if j >= 1:
        dee = (parse(time_data[j]) - parse(time_data[j - 1])).total_seconds()
        # print(dee)
        if dee <= 1800:
            dee = dee
            total_sec += dee
            # print(j, dee)

        else:  # 时间大于30分钟就不要这段时间了
            dee = 0
            total_sec = total_sec
            # print(j, dee)

    else:
        session_count += 1
        dee = 0
        # print(j, dee)
    diff_time.append(dee)
df['diff_time'] = diff_time

# print(diff_time)

# print(df)
# print(session_count)
# print(total_sec)
# 根据其他字段的值判断那两个数据相减

url_datas = df['$url']
# url不一样的是第几条数据，取出来
diffrent_url_no = []
url_no_list = []
url_no = 0

for i in range(len(url_datas)):
    if i > 0 and url_datas[i] == url_datas[i - 1]:  # 与上一条数据一样就继续
        # 新增一个字段赋值，url_no
        url_no = url_no
        url_no_list.append(url_no)
        continue
    elif i == 0:
        url_no = 0
        url_no_list.append(url_no)

        continue
    else:
        url_no += 1
        diffrent_url_no.append(i)
        url_no_list.append(url_no)
        continue
df['url_no_list'] = url_no_list
# print(url_no_list)
# print(diffrent_url_no)
print('共访问了{}个页面'.format(len(diffrent_url_no) + 1))
# print(df[:13]['diff_time'])
# print(df['diff_time'])
# 设置一个字段存放总计，如果不是diffrent_url_no中的位置则为空，是的话则显示总计
print(np.zeros(len(url_datas)))

sum_data_list = []
sum_data = 0
for z in range(len(diffrent_url_no) + 1):
    if z == 0:
        # print(df[:diffrent_url_no[z] + 1]['diff_time'])
        sum_data = df[:diffrent_url_no[z] + 1]['diff_time'].sum()
        # df[:diffrent_url_no[z]]['sum_data'] = 0
        df.loc[diffrent_url_no[z], 'SumDiffTime'] = sum_data
    elif z == len(diffrent_url_no):
        # print(df[diffrent_url_no[z - 1] + 2:]['diff_time'])
        sum_data = df[diffrent_url_no[z - 1] + 2:]['diff_time'].sum()
        # df[diffrent_url_no[z - 1] + 2:-2]['sum_data'] = 0
        df.loc[-1, 'SumDiffTime'] = sum_data
    else:
        # print(df[diffrent_url_no[z - 1] + 2:diffrent_url_no[z]]['diff_time'])
        sum_data = df[diffrent_url_no[z - 1] + 2:diffrent_url_no[z]]['diff_time'].sum()
        # df[diffrent_url_no[z - 1] + 2:diffrent_url_no[z] - 1]['sum_data'] = 0
        df.loc[diffrent_url_no[z], 'SumDiffTime'] = sum_data

# print(df['diff_time'], df['url_no_list'])
# new_series = df.groupby(by=['url_no_list'])['diff_time'].sum()
# print(new_series)
# df = df.reindex(columns=col_name)

df.to_csv(file_name, index=False)
