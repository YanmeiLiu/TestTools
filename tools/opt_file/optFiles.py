#!/usr/bin/python
# -*- coding: UTF-8 -*-
# update_time :2021-8-31
# 打开文件，补齐日期
import re
import time
import urllib.parse
from pathlib import Path

import pandas as pd

from config.setconfig import myconf, get_dir
from tools.compare_lists import ltLists
from tools.compile_projectid.dianping_crypto import decode_id


def data_clean(text):
    # 清洗excel中的非法字符，都是不常见的不可显示字符，例如退格，响铃等
    ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
    # print(ILLEGAL_CHARACTERS_RE.findall(text))
    if len(ILLEGAL_CHARACTERS_RE.findall(str(text))) > 0:
        text = ILLEGAL_CHARACTERS_RE.sub(r'', str(text))
    # print(text)
    return text


# 将df保存入文件
def writeToExcelFile(df, file_name, sheet_name=''):
    if isinstance(df, pd.DataFrame):  # 判断df是dataframe格式
        if file_name.endswith('.csv'):
            file_name = file_name[:-4] + '.xlsx'
        # 判断文件是否存在
        my_file = Path(file_name)
        if my_file.exists():
            # 不论是否有非法字符，都先洗一下
            print('开始写入:{}-{}'.format(file_name, sheet_name))
            # df = df.fillna('').astype(str)
            for col in df.columns:
                df[col] = df[col].apply(lambda x: data_clean(x))
            with pd.ExcelWriter(file_name, mode='a', engine='openpyxl') as writer:
                if sheet_name == '':
                    df.to_excel(writer, sheet_name='sheet', index=True)
                else:
                    df.to_excel(writer, sheet_name=sheet_name, index=True)

            print('结束写入:{}-{}'.format(file_name, sheet_name))
        else:
            # 不论是否有非法字符，都先洗一下
            print('开始写入:{}-{}'.format(file_name, sheet_name))
            # df = df.fillna('').astype(str)
            for col in df.columns:
                df[col] = df[col].apply(lambda x: data_clean(x))
            with pd.ExcelWriter(file_name, mode='w', engine='openpyxl') as writer:
                if sheet_name == '':
                    df.to_excel(writer, sheet_name='sheet', index=True)
                else:
                    df.to_excel(writer, sheet_name=sheet_name, index=True)
            print('结束写入:{}-{}'.format(file_name, sheet_name))
    else:
        print('writeToExcelFile_不是df格式！')


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
    # print(new_df)
    return new_df


# 比较表中col1列中的数据是否存在于clo2列中
def CompareColums(df, col1, col2):
    # 判断df是不是dataframe个格式
    if isinstance(df, pd.DataFrame):
        # 判断列名是否在df中存在
        # 获取列名
        col_name = df.columns.tolist()  # 将数据框的列名全部提取出来存放在列表里
        if col1 in col_name and col2 in col_name:
            print('开始比较')
            print(df[col1].isnull())
            print(df[col2].str.isdecimal())

            if df[col1].str.isdecimal():
                print('1')
                df['result'] = df.apply(
                    lambda x: 'yes' if x[col1] in df[col2].values else 'no', axis=1)
            else:
                df['result'] = df.apply(
                    lambda x: 'yes' if x[col1] is not None and x[col1] in df[col2].values else (
                        '' if x[col1] is None else 'no'),
                    axis=1)
            print('结束比较')
            return df
        else:
            # print('该列列名错误，请检查')
            return '该列列名错误，请检查'
    else:
        # print('格式不对')
        return '格式不对'


def ReplaceContent(restr, content, replacestr):
    if content:
        I_RE = re.search(restr, content, re.IGNORECASE)
        # 如果匹配中了，则替换成目标文字
        if I_RE:
            content = replacestr
        else:
            content = content
    return content


# col1是要修改的字段，根据字段col进行判断，若col 有值且存在判断依据则根据col字段进行正则匹配判断
def ReplaceAll(df, col1, restr, replacestr, col=None, col_data=None, re_match='yes'):
    # 判断df是不是dataframe格式
    if isinstance(df, pd.DataFrame):
        # 判断列名是否在df中存在
        # 获取列名
        col_name = df.columns.tolist()  # 将数据框的列名全部提取出来存放在列表里
        if col1 in col_name:
            # new_col = 'new_' + str(replacestr)
            # col_name.insert(-1, new_col)
            if col is None:
                df[col1] = df[col1].apply(
                    lambda x: replacestr if re.search(str(restr), str(x), re.IGNORECASE) else x)
                return df
            else:

                if re_match == 'yes':
                    df[col1] = df.apply(
                        lambda x: replacestr if re.search(str(col_data), str(x[col]),
                                                          re.IGNORECASE) and re.search(restr,
                                                                                       str(x[col1]),
                                                                                       re.IGNORECASE) else
                        x[col1],
                        axis=1)
                    return df
                else:
                    df[col1] = df.apply(
                        lambda x: replacestr if not re.search(str(col_data), str(x[col]),
                                                              re.IGNORECASE) and re.search(restr,
                                                                                           str(x[col1]),
                                                                                           re.IGNORECASE) else x[col],
                        axis=1)
                    return df

        else:
            # print('该列列名错误，请检查')
            return '该列列名错误，请检查'
    else:
        # print('格式不对')
        return '格式不对'


def ReplaceText(df, sa_metadata, cols=0):
    # 修改表头或者列表内容
    # 将文件中的不可读文案转为可读文案
    cf = myconf()
    config_file = 'sa.ini'
    config_path = get_dir('config', config_file)
    cf.read(config_path)
    if cols == 0:
        df.rename(columns=dict(cf.items(sa_metadata)), inplace=True)
    else:
        before_lists = []
        expect_lists = []
        for k, v in cf.items(sa_metadata):
            before_lists.append(k)
            expect_lists.append(v)
        df[cols].replace(before_lists, expect_lists, inplace=True)
    return df


# 取一个时间字段的一部分保存到另一个字段
def getPartTime(df, col, strtype):
    # 判断df是不是dataframe个格式
    if isinstance(df, pd.DataFrame):
        # 判断列名是否在df中存在
        # 获取列名
        col_name = df.columns.tolist()  # 将数据框的列名全部提取出来存放在列表里

        if col in col_name:
            # 转为时间格式
            df[col] = pd.to_datetime(df[col])
            if strtype == 'time':
                new_col = str(col) + '_time'
                df[new_col] = df[col].dt.time
            elif strtype == 'date':
                new_col = str(col) + '_date'
                df[new_col] = df[col].dt.date
            elif strtype == 'year':
                new_col = str(col) + '_year'
                df[new_col] = df[col].dt.year
            elif strtype == 'quarter':
                new_col = str(col) + '_quarter'
                df[new_col] = df[col].dt.quarter
            elif strtype == 'month':
                new_col = str(col) + '_month'
                df[new_col] = df[col].dt.month
            elif strtype == 'week':
                new_col = str(col) + '_week'
                df[new_col] = df[col].dt.week
            elif strtype == 'day':
                new_col = str(col) + '_day'
                df[new_col] = df[col].dt.day
            elif strtype == 'hour':
                new_col = str(col) + '_hour'
                df[new_col] = df[col].dt.hour
            elif strtype == 'minute':
                new_col = str(col) + '_minute'
                df[new_col] = df[col].dt.minute
            elif strtype == 'second':
                new_col = str(col) + '_second'
                df[new_col] = df[col].dt.second
            elif strtype == 'dayofyear':
                new_col = str(col) + '_dayofyear'
                df[new_col] = df[col].dt.dayofyear
            elif strtype == 'weekofyear':
                new_col = str(col) + '_weekofyear'
                df[new_col] = df[col].dt.weekofyear
            elif strtype == 'dayofweek':
                new_col = str(col) + '_dayofweek'
                df[new_col] = df[col].dt.dayofweek
            elif strtype == 'days_in_month':
                new_col = str(col) + '_days_in_month'
                df[new_col] = df[col].dt.days_in_month
            elif strtype == 'weekday_name':
                new_col = str(col) + '_weekday_name'
                df[new_col] = df[col].dt.weekday_name

            return df
        else:
            return '列名错误！'


# 将excel表中数字太长导致的使用科学计数法展示的不精确数字展示出来
def ConversionBigNum(df, col):
    if isinstance(df, pd.DataFrame):
        # 获取所有列名
        col_name = df.columns.tolist()
        if col in col_name:
            new_col = 'new_' + str(col)
            col_name.insert(1, new_col)
            i_list = []
            for i in df[col]:
                i = "'" + str(i)
                i_list.append(i)
            df[new_col] = i_list
            return df
    return


def SpiltItem(df, col, split_str=''):
    # 按照col将字段切割成多个
    """
    :param df:
    :param col: 被切割的字段
    :return:
    """
    # 判断df是不是dataframe个格式
    if isinstance(df, pd.DataFrame):
        # 判断列名是否在df中存在
        # 获取所有列名
        col_name = df.columns.tolist()
        if col in col_name:
            data_list = df[col].str.split(split_str, expand=True)
            print(data_list)
            for i in range(data_list.shape[1]):
                # print(type(data_list[i]))
                if data_list[i].all() != '':
                    new_col = str(col) + '_' + str(i)
                    df[new_col] = data_list[i].astype(str)
            # print(df)
            return df
        return


def ReadFileAsDF(file_name, sheet_name=None):
    # 判断文件是否存在
    my_file = Path(file_name)
    if my_file.exists():
        # 判断文件的格式
        if file_name.endswith('.csv'):
            # df = pd.read_csv(file_name, low_memory=False).astype(str) # 强制转为str类型
            df = pd.read_csv(file_name, low_memory=False)
            return df
        elif file_name.endswith('.xlsx'):
            # df = pd.read_excel(file_name, sheet_name=sheet_name).astype(str) # 强制转为str类型
            df = pd.read_excel(file_name, sheet_name=sheet_name)
            return df
        else:
            mes = '文件格式不对，请使用.csv或.xlsx后缀的文件'
            return mes
    else:
        mes = str(my_file) + '文件不存在'

        return mes


# 判断是否是工作时间
def SignText(df, col):
    # 判断df是不是dataframe个格式
    if isinstance(df, pd.DataFrame):
        # 判断列名是否在df中存在
        # 获取所有列名
        col_name = df.columns.tolist()
        if col in col_name:
            print(df[col])
            df['result'] = df.apply(lambda x: 'no' if 0 <= x[col] <= 7 or 20 <= x[col] <= 23 else 'yes', axis=1)
        return df
    else:
        return 'df不对！'


# 补充
def FillNa(df, col=None, fill_type=None, values=0):
    if isinstance(df, pd.DataFrame):
        # 判断列名是否在df中存在
        if col is None:
            df = df.fillna(value=values)
            return df
        else:
            # 获取所有列名
            col_name = df.columns.tolist()
            if col in col_name:
                if fill_type is None:
                    df[col] = df[col].fillna(value=values)
                # df.fillna(method=’ffill’)可以简写为df.ffill()
                elif fill_type == 'ffill':  # 使用前一个有效值填充
                    df = df.ffill()
                elif fill_type == 'bfill':  # 使用后一个有效值填充
                    df = df.bfill()
                else:
                    print('填充方式可以为空，或ffill，或bfill')
                return df
            else:
                return '列名错误！'
    else:
        return 'df错啦！'


def getPartStr(df, col, start_num):
    if isinstance(df, pd.DataFrame):
        col_name = df.columns.tolist()
        if col in col_name:
            new_col = str(col) + '_new'
            # df[new_col] = df[col].str.extract(r'\d{10,}(,\d+)*$', expand=False)
            df[new_col] = df.apply(lambda x: x[col][start_num:] if x[col] else '', axis=1)
            return df
        else:
            return '列名错误！'
    else:
        return 'df错啦！'


# 将url_path中的数字地址转为数据库中的ID
def turnToID(df, col):
    if isinstance(df, pd.DataFrame):
        col_name = df.columns.tolist()
        if col in col_name:
            # 取纯数字
            df[str(col) + '_id'] = df[col].str.extract(r'(\d+)', expand=False)
            print(df)
            df[str(col) + '_new'] = df.apply(lambda x: decode_id(x[str(col) + '_id']) if x[col] else 0, axis=1)
            return df
        else:
            return '列名错误！'
    else:
        return 'df错啦！'


# 根据一个字段的不同取值分割成不同的df 并保存下来
def SplitDataToDF(df, col):
    if isinstance(df, pd.DataFrame):
        # 判断列名是否在df中存在
        # 获取所有列名
        col_name = df.columns.tolist()
        if col in col_name:
            listType = df[col].unique()
            print(listType)
            for i in range(len(listType)):
                new_df = df[df[col].isin([listType[i]])]
                # # 保存处理好文件
                write_name = 'query_result.xlsx'
                write_file = get_dir('data_files/user_event', write_name)

                writeToExcelFile(new_df, write_file, sheet_name=str(listType[i]))
        else:
            return '列名错误！'
    else:
        return 'df错啦！'


# 分组查询
def SplitDataToCal(df, cols, calcols):
    """
    select userid,date,count(distinct(distinct_id)) users from events
    where  $url_host ='qs.36dianping.com' and date>='2021-9-1'  and userid >10000000000 group by userid,date ;
    """
    if isinstance(df, pd.DataFrame):
        # 判断列名是否在df中存在
        # 获取所有列名
        col_name = df.columns.tolist()
        # 参数格式：cols=['userid','monty']
        if ltLists(cols, col_name):
            # new_df = df.groupby(cols)['users'].sum()
            # new_df = df.groupby(cols)['users'].agg({'mean': np.mean, 'count': np.std})
            # calcols={'users': ['sum', 'count', np.mean]}
            new_df = df.groupby(cols).agg(calcols)
            return new_df
        else:
            return '列名错误！'
    else:
        return 'df错啦！'


# 按照字段切割df ,返回一个df_list
def groupByItem(df, cols):
    if isinstance(df, pd.DataFrame):
        # 判断列名是否在df中存在
        # 获取所有列名
        col_name = df.columns.tolist()
        if ltLists(cols, col_name):
            # df_list
            df_list = []
            col_ = df[cols].unique()
            for col in col_:
                temp_data = df[df[cols].isin([col])]
                # 生成一个字典，分组名：分组结果
                temp_dict = {col: temp_data}
                df_list.append(temp_dict)
            return df_list
        else:
            return
    else:
        return


# 合并两个df
def MergetDF(df1, df2, cols, how):
    if isinstance(df1, pd.DataFrame) and isinstance(df2, pd.DataFrame):
        # 判断列名是否在df中存在
        # 获取所有列名
        col_name1 = df1.columns.tolist()
        col_name2 = df2.columns.tolist()
        a = ltLists(cols, col_name2)
        # print(a)
        if ltLists(cols, col_name1) and ltLists(cols, col_name2):
            # 按照cols合并
            # 合并项如果是不同数据类型的话会出错，所以还要统一类型
            for col in cols:
                if df1[col].dtype != df2[col].dtype:
                    df1[col] = df1[col].apply(str)
                    df2[col] = df2[col].apply(str)

            new_df = pd.merge(df1, df2, on=cols, how=how)
            return new_df
        else:
            return 'df的列名错误'
    else:
        return 'df错啦！'


# 计算df中两列数据的时间差
def calTime(df, col1, col2):
    if isinstance(df, pd.DataFrame):
        col_name = df.columns.tolist()
        if col1 in col_name and col2 in col_name:
            df[col1] = pd.to_datetime(df[col1])
            df[col2] = pd.to_datetime(df[col2])
            df['diff_time'] = df[col1] - df[col2]
            # print(df[col2])
            # print(df['diff_time'])
            # 计算全部秒
            df['diff_time(s)'] = df['diff_time'].dt.total_seconds()
            # 秒转为小时
            df['diff_time(h)'] = round(df['diff_time(s)'] / 3600, 2)
            # 将时间差全部保存下来，去掉毫秒，因为不转为str保存的话只能保存到文件中"天数"
            df['diff_time'] = pd.to_timedelta(df['diff_time'])
            df['diff_time'] = df['diff_time'].astype('str')
            df['diff_time'] = df['diff_time'].apply(lambda x: x.split('.')[0])
            # print(df['diff_time'])
            return df
        else:
            return 'df的列名错误'
    else:
        return 'df错啦！'


# 时间戳转为规范时间
def time_c(timeNum):
    timeTemp = float(timeNum / 1000)
    tupTime = time.localtime(timeTemp)
    stadardTime = time.strftime("%Y-%m-%d %H:%M:%S", tupTime)
    return stadardTime


# 行转列——某些列转换为表头
def pivotdf(df, index_cols, transfer_col, data_col):
    if isinstance(df, pd.DataFrame):
        df = pd.pivot(data=df,  # 待转换df
                      index=index_cols,  # df交叉后行
                      columns=transfer_col,  # df交叉后的列
                      values=data_col  # df交叉后数据（不发生聚合）
                      )
        df = FillNa(df)
        # df = df.reset_index(inplace=True)
        # print(df)
        return df
    else:
        return


# 两个字段合并成一个字段
def ItemJoin(df, col1, col2):
    if isinstance(df, pd.DataFrame):
        col_name = df.columns.tolist()
        if col1 in col_name and col2 in col_name:
            # 合并两列
            df[col1 + '-' + col2] = df[col1] + '-' + df[col2]
            #     删除两列
            df = df.drop(columns=[col1, col2])
            return df
        else:
            return 'df的列名错误'
    else:
        return


# 日期转时间戳
def mktimeDF(df, time_col, type='date'):
    if isinstance(df, pd.DataFrame):
        col_name = df.columns.tolist()
        if time_col in col_name:
            if type == 'date':
                df['timestamp'] = df[time_col].apply(lambda x: time.mktime(time.strptime(x, '%Y-%m-%d')) * 1000)
                return df
            if type == 'time':
                df['timestamp'] = df[time_col].apply(lambda x: time.mktime(time.strptime(x, '%Y-%m-%d %H:%M:%S')))
                return df
            else:
                return 'type错误，使用date or time'
        else:
            return 'df的列名错误'
    else:
        return


def unquoteurl(df, col, type):
    if isinstance(df, pd.DataFrame):
        col_name = df.columns.tolist()
        if col in col_name:
            if type == 'unquote':
                df['unquote'] = df[col].astype(str).apply(lambda x: urllib.parse.unquote(x))
                return df
            if type == 'quote':
                df['quote'] = df[col].astype(str).apply(lambda x: urllib.parse.quote(x))
                return df
            else:
                return 'type错误，使用 unquote or quote'
        else:
            return 'df的列名错误'
    else:
        return


# 扩充时间序列
def RangeDate(df, col=None, col_date='c_date'):
    items_ = df[col].unique()  # 拆成不同的数据段
    last_df = pd.DataFrame(columns=df.columns)
    for item in items_:
        item_df = df[df[col].isin([item])]
        date_range = pd.date_range(start=item_df[col_date].min(), end='2023-02-01',
                                   freq="D")  # freq="D"表示按天，可以按分钟，月，季度，年等
        temp_df = item_df.set_index(col_date).reindex(index=date_range)
        # 补充值
        temp_df = FillNa(temp_df, col, None, item)
        temp_df = FillNa(temp_df, 'day_comments', None, 0)
        temp_df = FillNa(temp_df, '截止到当天点评数', 'ffill')
        last_df = pd.concat([last_df, temp_df], axis=0)
    return last_df


# 将url_path中的数字地址转为数据库中的ID
def comStr(df, col1, col2):
    if isinstance(df, pd.DataFrame):
        col_name = df.columns.tolist()
        if col1 in col_name and col2 in col_name:
            # 取纯数字
            df['result'] = df.apply(lambda x: (x[str(col) + '_id']) if x[col] else 0, axis=1)
            return df
        else:
            return '列名错误！'
    else:
        return 'df错啦！'


if __name__ == '__main__':
    file_1 = get_dir('data_files/user_event', '产品详细信息_crosstab.xlsx')
    # file_2 = get_dir('data_files/user_event', '执行结果1 (33).csv')
    df1 = ReadFileAsDF(file_1, '产品详细信息_crosstab')
    df2 = ReadFileAsDF(file_1, 'lz')
    # df3 = ReadFileAsDF(file_1, '3')
    # df4 = ReadFileAsDF(file_1, '4')
    # df5 = ReadFileAsDF(file_1, '5')
    # df6 = ReadFileAsDF(file_1, '6')
    # df7 = ReadFileAsDF(file_1, 'rank')
    # df8 = ReadFileAsDF(file_1, 'func')
    # df9 = ReadFileAsDF(file_1, 'dianping')
    # df10 = ReadFileAsDF(file_1, 'searchresult')
    # df11 = ReadFileAsDF(file_1, 'land-page')
    # df12 = ReadFileAsDF(file_1, 'evaluation')

    # df3 = ReadFileAsDF(file_1, '915')

    # df = ItemJoin(df1, '留资时间点', '是否留资产品')
    # df = mktimeDF(df, time_col='公历日期')
    # df = pivotdf(df1, index_cols=['score'], transfer_col='group_num', data_col='点评数')
    # df = getPartStr(df, '站内链接',26)
    # df = getPartStr(df, 'url_path', 7)
    # new_df = turnToID(df1, '$url_path')
    # df['分组1替换'] = ReplaceContent('baidu', content, '站外搜索')
    # df1 = SpiltItem(df1, 'title', '-36')

    # filename = '123.csv'
    # file_name = get_dir('data_files/user_event', filename)
    #
    # df2 = ReadFileAsDF(file_name, sheet_name='sheet3')
    # df2 = ReadFileAsDF(file_name, sheet_name='sheet5')
    # print(df2)
    # new_df = getValue(df1, df2, 'mobile')
    # print(m)
    # new_df = calTime(df, 'submit_time', 'time')
    # new_df = MergetDF(df1, df2, ['id'], 'left')
    # print(new_df)
    # 去掉id列中重复的行，并保留重复出现的行中第一次出现的行
    # new_df = new_df.drop_duplicates(subset=['id'], keep='first')
    # 页面路径补充完整
    # print(new_df['页面地址路径'])
    # new_df['url'] = new_df.apply(
    #     lambda x: str('https://www.36dianping.com') + str(x['页面地址路径']) if x['页面地址路径'] is not None else '/',
    #     axis=1)
    #
    # print(new_df)

    # print(df)
    # print(df['time'])
    # new_df = CompareColums(df1, '登录2', '登录1')
    # new_df = ComplateDate(df, 'date(created_at)', '2021-7-22', '2021-10-20')
    # new_df = ConversionBigNum(df1, 'user_id')
    # print(new_df['second_id'].dtype)
    #
    # # new_df['second_id'] = new_df['second_id'].astype(int)
    #
    # filename = '20211207_061832.xlsx'
    # file_name = get_dir('data_files/user_event', filename)
    #
    # df2 = ReadFileAsDF(file_name, sheet_name='sheet1')
    # print(df2['second_id'].dtype)
    # try:
    #     df2['second_id'] = df2['second_id'].astype(str)
    # except Exception as e:
    #     print(e)
    #
    # df1 = RangeDate(df1, 'product_id')
    new_df = MergetDF(df1, df2, ['product_id'], 'left')
    # new_df = MergetDF(new_df, df3, ['project_id'], 'outer')
    # new_df = MergetDF(new_df, df4, ['project_id'], 'outer')
    # new_df = MergetDF(new_df, df5, ['project_id'], 'outer')
    # new_df = MergetDF(new_df, df6, ['project_id'], 'outer')
    # new_df = MergetDF(new_df, df7, ['date'], 'outer')
    # new_df = MergetDF(new_df, df8, ['date'], 'outer')
    # new_df = MergetDF(new_df, df9, ['date'], 'outer')
    # new_df = MergetDF(new_df, df10, ['date'], 'outer')
    # new_df = MergetDF(new_df, df11, ['date'], 'outer')
    # new_df = MergetDF(new_df, df12, ['date'], 'outer')

    # df23 = MergetDF(df12, df3, ['qa_id'], 'left')
    # df = SplitDataToCal(new_df, ['project_id', 'name', '首次上线时间'], {'pv': ['sum'], 'uv': ['sum']})
    # new_df = getPartTime(df, 'date', 'month')
    # print(new_df)
    # new_df = getPart(new_df, 'time_t', 'hour')
    # new_df = FillNa(new_df, 'day_comments')
    #
    # new_df = FillNa(new_df, '截止到当天点评数', 'ffill')
    # new_df = FillNa(new_df, 'lz_uv')
    # new_df = unquoteurl(df1, 'keywords', 'unquote')
    # new_df = SignTexct(df, 'new_time')
    # df2.drop_duplicates(subset=['userid'], keep='first', inplace=True)
    # write_name='11.xlsx'
    # write_name = get_dir('data_files/user_event', write_name)
    # new_df = SplitDataToCal(new_df, ['userid', 'date_month'])
    writeToExcelFile(new_df, file_1, sheet_name='sheet')
