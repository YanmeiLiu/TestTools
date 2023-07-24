import pandas as pd
from pandas._libs.tslibs.offsets import CustomBusinessDay

from config.setconfig import get_dir

file_name = get_dir('results_file', 'read_IP.xlsx')
df = pd.read_excel(file_name, '明细数据')
print(df.head())
print(df.shape)
print(df.index)
# 加载时间序列
print('#' * 100)
df1 = pd.read_excel(file_name, '明细数据', parse_dates=['行为时间'], index_col='行为时间')
print(df1.index)
# print(df1.tail())
# print(df1["2021-06-30":"2021-07-01"]['IP'])
print(df1.IP.resample('M'))
import matplotlib

# df1.IP.plot()


df3 = pd.read_excel(file_name, 'Sheet1', header=None, names=['IP', 'Count'])
print(df3)
rng = pd.date_range(start='2021-6-1', end='2021-6-15', freq='B')
print(rng)
df3.set_index(rng, inplace=True)
print(df3)

# 节假日
print('#' * 100)
df4 = pd.read_excel(file_name, 'Sheet1', header=None, names=['IP', 'Count'])
print(df4)
rng4 = pd.date_range(start='5/1/2017', end='21/5/2017', freq='B')
print(rng4)
from pandas.tseries.holiday import AbstractHolidayCalendar, nearest_workday, Holiday


class myCal(AbstractHolidayCalendar):
    rules = [Holiday('劳动节', month=5, day=1), Holiday('mybirth', month=5, day=11)]


wuyi = CustomBusinessDay(calendar=myCal())
rng5 = pd.date_range(start='5/1/2017', end='21/5/2017', freq=wuyi)
print('有五一劳动节', rng5)
# 埃及工作日 星期日到星期四
egypt_weekdays = "Sun Mon Tue Wed Thu"
b2 = CustomBusinessDay(weekmask=egypt_weekdays)
rng6 = pd.date_range(start='5/1/2017', end='21/5/2017', freq=b2)
print('埃及工作日', rng6)

#
from datetime import datetime

dt = datetime(2017, 5, 1)
print(dt + 3 * b2)


