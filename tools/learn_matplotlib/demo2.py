# 柱状图
import matplotlib.pyplot as plt
import matplotlib.animation as ani

import pandas as pd
import numpy as np
from collections import Counter

from config.setconfig import get_dir

file_name = get_dir('data_files', 'LanguageWorkedWith.csv')
df = pd.read_csv(file_name)
print(df.head())

plt.style.use('ggplot')
ids = df['Response_id']
print(ids)
language_response = df['LanguageWorkedWith']
print(type(language_response))
list_lgg = language_response[:5]
# for example
lsit1 = [1, 1, 2, 3, 1, 1, 2]
cnt = Counter()
for i in lsit1:
    cnt.update(str(i))

print(cnt)
#
cnt_language = Counter()
for i in language_response:
    cnt_language.update(i.split(';'))
print(cnt_language)
# 频次最高的5项
most_num = cnt_language.most_common(11)
language = []
population = []
for i in most_num:
    language.append(i[0])
    population.append(i[1])

print(language)
print(population)
plt.figure(figsize=(20,20))
# plt.bar(language, population)
# 横向模式
# 列表做反向,数据最多的在上面
language.reverse()
population.reverse()
plt.barh(language, population)

plt.rcParams['font.sans-serif'] = ['SimHei'] # 处理中文
plt.title('编程语言')
plt.xlabel('语言')
plt.ylabel('人次')
plt.savefig('language.png')

plt.show()
animator = ani.FuncAnimation(fig, chartfunc, interval = 100)
