import matplotlib.animation as ani
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

from config.setconfig import get_dir
from tools.opt_file.optFiles import ReadFileAsDF, writeToExcelFile, time_c

# 第一步：一次性操作
# 获取数据
# url = 'https://lab.isaaclin.cn/nCoV/api/area'
# res = requests.get(url)
# res = res.json()
# result = res['results']
# # 转为pd
# df = pd.DataFrame(result)
# # 保存
write_name = 'xinguan_datas.xlsx'
write_name = get_dir('data_files/user_event', write_name)
# writeToExcelFile(df, write_name, sheet_name='sheet')

filename = 'xinguan_datas.xlsx'
file_name = get_dir('data_files/user_event', filename)

df = ReadFileAsDF(file_name, sheet_name='sheet1')

#
# df_interest = df.loc[df['continentName'].isin(['亚洲']) & df['updateTime'].isna()]
df_interest = df.loc[df['continentName'].isin(['亚洲'])]

# # 转时间
#
df['updateTime'] = df_interest['updateTime'].apply(time_c)
print(df_interest)
#
# df_interest.rename(
#     index=lambda x: df_interest.at[x, 'countryName'], inplace=True)
# print(df_interest)
# df1 = df_interest.transpose()
print(df)
writeToExcelFile(df, write_name, sheet_name='sheet')

# df1 = df1.drop(['continentName', 'updateTime'])
# df1 = df1.loc[(df1 != 0).any(1)]
# df1.index = pd.to_datetime(df1.index)
