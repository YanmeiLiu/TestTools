import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

from config.setconfig import get_dir

file_name = get_dir('data_files', 'from_zhanwai_users.xlsx')
df = pd.read_excel(file_name, 'Sheet1')

from_zhanwai = df['from_zhanwai']
users = df['users']
df.sort_values(by='users')
except_df = df.query()

zhanshi_df = df.head(10)
qita_df = df.tail(93)
qita = qita_df['users'].sum()
qita_data=pd.DataFrame({'from_zhanwai':'qita',
                  'users':qita},
                 index=[1])   # 自定
zhanshi_df=zhanshi_df.append(qita_data,ignore_index=True)   # ignore_index=True,表示不按原来的索引，从0开始自动递增
print(zhanshi_df)
plt.rcParams['font.sans-serif'] = ['SimHei']
# 选择人数最多的前10项
# plt.xticks(x, labels=pdates)
plt.legend()
# 扇形图
plt.pie(zhanshi_df['users'], labels=zhanshi_df['from_zhanwai'],pctdistance=0.8,autopct='%.1f%%' )
plt.show()
