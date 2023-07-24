import pandas as pd

# 使用csv读取
from config.setconfig import get_dir

file_name = get_dir('results_file/spider', 'baidu_20210628164104.csv')
df = pd.read_csv(file_name)
print(df.columns)

# excel读取
excel_file_name = get_dir('results_file', 'read_IP.xlsx')
print(excel_file_name)
df2 = pd.read_excel(excel_file_name, 'Sheet1', header=None)
# 设置表头字段信息
df2.columns = ['IP段', '数量']
print(df2.head(4))

# 使用字典模式
weather_data = {
    'day': ['2021-7-1', '2021-7-2', '2021-7-3', '2021-7-4', '2021-7-5'],
    'temperature': [32, 31, 34, 23, 30],
    'wind_speed': [6, 3, 5, 4, 2]
}
print(weather_data)
df3 = pd.DataFrame(weather_data)
print(df3)

event = ['Rain', 'Snow', 'Sun', 'Cloud', 'Sun']
# 增加第4个字段
df3['event'] = event
print(df3)

# 元组列表
weather_data = [('2021-8-1', 32, 6, 'Rain'), ('2021-8-2', 12, 6, 'Rain'), ('2021-8-3', 30, 6, 'Rain'),
                ('2021-8-4', 29, 6, 'Rain')]
df4 = pd.DataFrame(weather_data)
df4.columns = ['day', 'temperature', 'wind_speed', 'event']
print(df4)

# 列表字典
weather_data = [{'day': '2021-9-1', 'temperature': 32, 'wind_speed': 6, 'event': 'Rain'},
                {'day': '2021-9-2', 'temperature': 33, 'wind_speed': 6, 'event': 'Rain'},
                {'day': '2021-9-3', 'temperature': 34, 'wind_speed': 6, 'event': 'Rain'},
                {'day': '2021-9-4', 'temperature': 35, 'wind_speed': 6, 'event': 'Rain'}, ]
df5 = pd.DataFrame(weather_data)
print(df5)
print(weather_data)
print(df5.shape)
# 索引访问
print(df5[1:2])
# 列访问
print(df5.day)
print('$' * 100)
print(df5[['day', 'wind_speed']])
print('#' * 100)
# 平均值
print(df5.wind_speed.mean())
# 最大值
print(df5.wind_speed.max())
# 创建索引
df5.set_index('day',inplace=True)
print(df5.index)


