from matplotlib import pyplot as plt
import matplotlib
import numpy as np

# print(matplotlib.__version__)
import pandas as pd

# x = [0, 1, 2, 3, 4]  # x轴数据
# y = [0, 1, 2, 2, 4]  # y轴数据

# plt.plot(x, y, marker='.', markersize=10, color='red', linewidth=1, markeredgecolor='blue')
plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.xlabel('x轴数据')
# plt.ylabel('y轴数据')
# plt.show()
dev_x = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
dev_y = [1125, 222, 2327, 3238, 4329, 343, 6551, 7452, 8323, 3400, 3500]
dev_py_y = [125, 226, 2127, 2138, 3429, 343, 651, 7452, 8243, 3400, 350]
dev_p_y = [1250, 2260, 2270, 2180, 3209, 3430, 6510, 7352, 843, 3000, 3050]
plt.subplot(1, 4, 1)
plt.plot(dev_x, dev_y, color='#942828', label='suo')
plt.subplot(1, 4, 2)
plt.plot(dev_x, dev_py_y, 'b^--', label='2')  # format =[blue][marker][line]
plt.subplot(1, 4, 3)
plt.plot(dev_x, dev_p_y, 'o--', color='#23a51b', label='2')  # format =[blue][marker][line]
plt.subplot(1, 4, 4)

plt.legend()  # 显示示例
plt.xlabel('Age')
plt.ylabel('count')
plt.title('title')
plt.grid()

print(plt.style.available)  # 全部风格
# plt.style.use('Solarize_Light2') #设置风格
# plt.rcParams['font.sans-serif'] = ['SimHei'] # 处理中文
plt.xkcd()  # 动漫风格，只适用于纯英文
plt.savefig('ds.png')
plt.show()

x = np.arange(0, 5, 0.1)
y = np.sin(x)
# c是color的简写，ls是linestyle的简写，lw是linewidth的简写

plt.plot(x, y, c='g', ls='dotted')
plt.savefig('ds.png')
plt.show()

x1 = np.arange(0, 10, 2)
x2 = np.arange(0, 20, 4)
y1 = np.sin(x1)
y2 = np.sin(x2)
plt.plot(x1, y1, x1, y2)
plt.title('test lines together', loc='center')  # loc 取值有 left,right,center
plt.xlabel('I am x ', loc='right')  # loc 取值有 left,right,center
plt.ylabel('I am y ', loc='bottom')  # loc 取值有 bottom,top,center

plt.show()
