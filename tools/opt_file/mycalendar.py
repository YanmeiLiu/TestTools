import pandas as pd
import requests
import json
import numpy as np
import re

from TestTools.config.setconfig import get_dir
from TestTools.tools.opt_file.optFiles import writeToExcelFile


# 生成某一年的日历
def gen_calendar2022(year=2022):
    df = pd.DataFrame()
    # 获取法定节假日
    up1 = 'https://sp1.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?tn=wisetpl&format=json&resource_id=39043&query='
    up2 = '月&t=1642579711570&cb=op_aladdin_callback1642579711570'
    # 2022年接口已经改为按月获取数据，因此循环12个月获取每月数据
    for i in range(1, 13):
        url = "".join([up1, str(year), "年", str(i), up2])
        print(url)
        r = requests.get(url)
        rtxt = re.split("[()]", r.text)[1]
        r_json = json.loads(rtxt)
        each_d1 = pd.DataFrame(r_json['data'])
        each_d2 = pd.DataFrame(each_d1['almanac'][0])
        ## 筛选当月数据，数据中year\month\day是公立日期，数据会返回3个月的数据
        each_d3 = each_d2[each_d2['month'] == str(i)]
        # ## 由于12月的数据没有status字段（可能是下一年一月放假规定没出来，所以这里进行特殊处理)--结论应该是某些月份没有节假日就没有status字段，所以后面专门针对status进行处理
        # if i==11:
        #     each_d3=each_d2[each_d2['month']>=str(i)]
        # else:
        #     each_d3=each_d2[each_d2['month']==str(i)]
        ## 组合真的日期，并标记节假日情况
        each_d3['公历日期'] = pd.to_datetime(each_d3['year'] + "/" + each_d3['month'] + "/" + each_d3['day'])
        each_d3['周几'] = each_d3['公历日期'].dt.dayofweek + 1
        ## 标记是否节假日(即当天是否是法定放假)，其中status中的1表示放假，2表示上班，注意需要处理有没有status列的情况
        ## 有status的情况
        if "status" in each_d3.columns:
            each_d3['status'].fillna(0, inplace=True)
            each_d3['status'] = each_d3['status'].astype('int', errors='ignore')
            ## 按周几把周末标记成1，周一至周五标记成0，然后通过标记和status的值相加，结果为1和2的就是假期
            judge = np.where(each_d3['周几'] < 6, 0, 1) + each_d3['status']
            each_d3['是否节假日'] = np.where((judge == 1) | (judge == 2), "Y", "N")
            df = pd.concat([df,each_d3],ignore_index=True)
            # each_d3.to_csv("百度日历.csv",index=False)
        ## 没有status的情况，直接按周末为节假日
        else:
            each_d3['是否节假日'] = np.where(each_d3['周几'] >= 6, "Y", "N")
            df = pd.concat([df,each_d3],ignore_index=True)
    # 重命名列
    df.rename(columns={'animal': '生肖', 'avoid': '忌', 'cnDay': '中文星期', 'day': '日', 'gzDate': '干支日',
                       'gzMonth': '干支月', 'gzYear': '干支年', 'isBigMonth': '是否为阴历大月', 'lDate': '中文阴历日',
                       'lMonth': '中文阴历月', 'lunarDate': '数字阴历日', 'lunarMonth': '数字阴历月',
                       'lunarYear': '数字阴历年', 'month': '月', 'oDate': '阳历当天0点', 'suit': '宜',
                       'term': '节气节日', 'type': '各种与节日有关的类型', 'value': '各种日', 'year': '年',
                       'desc': '一种节日', 'status': '1休假2上班'},
              inplace=True)
    return df


if __name__ == "__main__":
    df = pd.DataFrame()
    for year in range(2022, 2024):
        # 注意2010年的元旦当天并未被百度标记为假日，所以当年的数据可能是错误的
        # year=2022
        each_df = gen_calendar2022(year)
        df = pd.concat([df,each_df],ignore_index=True)
    write_file=get_dir('data_files/user_event', '节假日.xlsx')
    writeToExcelFile(df, write_file, sheet_name='年节日历表')

