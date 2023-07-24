import pandas as pd
import numpy as np

# 使用csv读取
from pandas._libs.tslibs.offsets import Hour

from config.setconfig import get_dir

base_name = 'time_release.xlsx'

file_name = get_dir('data_files', base_name)
df = pd.read_excel(file_name)
# print(df.head(2)['action_time'])
action_time = df['action_time']
# print(action_time)
# 取开始时间
# start_list = []
# end_list = []
# hour_list = []
# for a in action_time:
#     start_at = a.split('~')[0]
#     end_at = a.split('~')[1]
#     start_list.append(start_at)
#     end_list.append(end_at)
#
# # 新增列 用于保存 计算过程和结果
# col_name = df.columns.tolist()  # 将数据框的列名全部提取出来存放在列表里
# col_name.insert(1, 'start_at')  # 开始时间
# col_name.insert(2, 'end_at')  # 结束时间
# df['start_at'] = start_list
# df['end_at'] = end_list
#
df['start_at'] = df['action_time'].str.split('~', expand=True, n=2)[0]
df['end_at'] = df['action_time'].str.split('~', expand=True, n=2)[1]

# 将str类型/object类型转换为datetime类型，强制转换，跳过错误

df['start_at'] = pd.to_datetime(df['start_at'], errors='coerce')
df["end_at"] = pd.to_datetime(df['end_at'], errors='coerce')
#
df['time'] = df['start_at'].dt.hour

# print(df.head(30))
df['sum'] = df.groupby('time')['num'].transform('sum')
print(df)
# 输出文件
with pd.ExcelWriter(file_name, mode='a', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='sheet', index=True)
