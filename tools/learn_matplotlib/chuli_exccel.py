import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from config.setconfig import get_dir

file_name = get_dir('data_files', '723-729.xlsx')
df = pd.read_excel(file_name, 'SheetJS')
plt.grid()
state = len(df['state'].unique())
print(state)
# 获取日期最大值和最小值
start_day = df['days'].min()
end_day = df['days'].max()

# 处理数据，将不同state所对应的值筛选出来
# state = 1
state_1 = df[df['state'] == 1][['days', 'count(*)']]
print('state_1', state_1)
print(state_1['days'])

# 补齐缺少的日期
# 设置索引
df_date = state_1.set_index("days")
# 将state_1的索引设置为日期索引
df_date = df_date.set_index(pd.to_datetime(df_date.index))
# 生成完整的日期序列，补齐数据
pdates = pd.date_range(start=start_day, end=end_day)
new_state_1 = df_date.reindex(pdates, fill_value=0)
print('new_state_1', '\n', new_state_1)
print(pdates)

# state = 2
state_2 = df[df['state'] == 2][['days', 'count(*)']]
print('state_2', state_2)
# 补齐缺少的日期
# 设置索引
df_date_2 = state_2.set_index("days")
# 将state_1的索引设置为日期索引
df_date_2 = df_date_2.set_index(pd.to_datetime(df_date_2.index))
# 生成完整的日期序列，补齐数据
pdates_2 = pd.date_range(start=start_day, end=end_day)
new_state_2 = df_date_2.reindex(pdates_2, fill_value=0)
# print('new_state_2', new_state_2)

# state = 0
state_0 = df[df['state'] == 0][['days', 'count(*)']]
# print('state_0', state_0)
# 补齐缺少的日期
# 设置索引
df_date_0 = state_0.set_index("days")
# 将state_1的索引设置为日期索引
df_date_0 = df_date_0.set_index(pd.to_datetime(df_date_0.index))
# 生成完整的日期序列，补齐数据
pdates_0 = pd.date_range(start=start_day, end=end_day)
new_state_0 = df_date_0.reindex(pdates_0, fill_value=0)
# print('new_state_0', new_state_0)

# 折线型
# plt.plot(pdates, new_state_1['count(*)'], 'b^--',)
# plt.plot(pdates_2, new_state_2['count(*)'], 'ro')
# plt.plot(pdates_0, new_state_0['count(*)'], 'g>-')
# plt.legend(('state=1', 'state=2', 'state=0'))
# 条形图型
bar_width = 0.2
x = np.arange(len(pdates))  # x轴刻度标签位置
print(x)

plt.bar(x - bar_width, new_state_0['count(*)'], bar_width, label='state=0')
# 给条形图添加数据标注
for m, y in enumerate(new_state_0['count(*)'].values):
    print(m, y)
    if y != 0:
        plt.text(m - bar_width, y, "%s" % y)

plt.bar(x, new_state_1['count(*)'], bar_width, label='state=1')
# 给条形图添加数据标注
for m, y in enumerate(new_state_1['count(*)'].values):
    print(m, y)
    if y != 0:
        plt.text(m, y, "%s" % y)
plt.bar(x + bar_width, new_state_2['count(*)'], bar_width, label='state=2')
# 给条形图添加数据标注
for m, y in enumerate(new_state_0['count(*)'].values):
    print(m, y)
    if y != 0:
        plt.text(m + bar_width, y, "%s" % y)
plt.xticks(x, labels=pdates)
plt.legend()
# 扇形图
plt.pie(new_state_1['count(*)'], labels=pdates, autopct='%.1f%%')
plt.show()
