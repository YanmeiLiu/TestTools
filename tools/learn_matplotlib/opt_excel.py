import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

from config.setconfig import get_dir


def opt_excelfile(filename, format):
    file_name = get_dir('data_files', filename)
    if format == 'excel':
        df = pd.read_excel(file_name)
        return df

    elif format == 'csv':
        df = pd.read_csv(file_name)
        return df

    else:
        print('格式请使用excel或csv!')
        return False


# 补齐缺少的日期
def ComplateDate(df, time_item, start_day, end_day):
    # 设置索引
    df_date = df.set_index(time_item)
    # 将state_1的索引设置为日期索引
    df_date = df_date.set_index(pd.to_datetime(df_date.index))
    # print(df_date)
    # 生成完整的日期序列，补齐数据
    pdates = pd.date_range(start=start_day, end=end_day)
    # print(pdates)
    new_df = df_date.reindex(pdates, fill_value=0)
    return pdates, new_df


if __name__ == '__main__':
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 处理中文
    df = opt_excelfile('8月份每日新增用户.xlsx', 'excel')
    created_at = df['created_at']
    kind = df['kind']
    num_kind_1 = df[df['kind'] == 1][['created_at', 'num']]
    num_kind_0 = df[df['kind'] == 0][['created_at', 'num']]
    print(num_kind_0)
    # 补齐时间
    # 获取日期最大值和最小值
    start_day = df['created_at'].min()
    end_day = df['created_at'].max()
    pdates, new_num_kind_0 = ComplateDate(num_kind_0, 'created_at', start_day, end_day)
    pdates, new_num_kind_1 = ComplateDate(num_kind_1, 'created_at', start_day, end_day)
    print(new_num_kind_0)
    x = np.arange(len(pdates))  # x轴刻度标签位置

    plt.plot(x, new_num_kind_0['num'], x, new_num_kind_1['num'])  # format =[blue][marker][line]
    plt.legend(('微信', '手机号'))  # 显示示例
    plt.xticks(x, labels=pdates)
    plt.xlabel('日期')
    plt.ylabel('注册数')
    plt.title('8月份每日新增注册用户')
    plt.grid()
    plt.show()
