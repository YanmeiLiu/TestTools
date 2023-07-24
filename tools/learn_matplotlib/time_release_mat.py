from matplotlib import pyplot as plt
import matplotlib
import pandas as pd
import numpy as np
import matplotlib.ticker as ticker

from config.setconfig import get_dir

base_name = 'time_release.xlsx'

file_name = get_dir('data_files', base_name)
df = pd.read_excel(file_name, sheet_name='sheet1')
plt.rcParams['font.sans-serif'] = ['SimHei']
time_hour = df.head(23)['time']
sum_num = df.head(23)['sum']
# 设置横轴显示密度

fig, ax = plt.subplots(1, 1)
tick_spacing = 1
for x, y in zip(time_hour, sum_num):
    plt.text(x, y + 0.05, '%.0f' % y, ha='center', va='bottom', fontsize=11)

ax.plot(time_hour, sum_num, 'o-', color='#23a51b', label='2')

ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
# plt.legend()  # 显示示例
plt.xlabel('hour', loc='right')
plt.ylabel('count', loc='center')
plt.title('按小时统计')
plt.grid()

print(plt.style.available)  # 全部风格

plt.xkcd()  # 动漫风格，只适用于纯英文
plt.savefig('ds.png')
plt.show()
