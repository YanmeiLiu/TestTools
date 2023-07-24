#!/usr/bin/python
# -*- coding: UTF-8 -*-
# update_time :2021-9-14
# 用户画像计算:数据库表中导数数据生成的excel文件，按照不同的字段分组取前N名的数据，后续N+1到最后一名的数据都是其他数据，计算占比

from TestTools.config.setconfig import get_dir
from TestTools.tools.opt_file.optFiles import ReadFileAsDF, writeToExcelFile
import pandas as pd
from matplotlib import pyplot as plt


class CalDataToShow(object):
    def __init__(self, filename, sheet_name=None, top_num=10, SumItem=None, *args):
        # 统计展示前top_num的数据
        self.top_num = top_num
        # 按照哪个字段求和
        self.SumItem = SumItem
        self.args = args
        self.file_name = get_dir('data_files', filename)
        self.df = ReadFileAsDF(self.file_name, sheet_name)

    # 获取数据
    def GroupDate(self):
        if isinstance(self.df, pd.DataFrame):  # 判断df是否是dataframe格式
            if self.args is None:
                return
            else:
                col_names = self.df.columns.tolist()  # 将数据框的列名全部提取出来存放在列表里
                # print(col_names)
                # 获取参数名
                group_cols = []
                # 形参是列表，将列表中的数据都拿出来看是否在df中存在，如果都存在则可以分组处理
                for group_col in self.args:
                    print('1111', group_col)
                    if group_col in col_names:
                        group_cols.append(group_col)
                        # 将为空的值处理成未知
                        self.df[group_col] = self.df[group_col].fillna(value='未知')
                    else:
                        # break
                        raise NameError(" 存在参数名错误.")
                # 分组
                # print(group_cols)
                new_df = self.df.groupby(group_cols)
                name_list = []
                data_list = []
                for name, data in new_df:
                    name_list.append(name)
                    # 按照哪个值计算
                    # 如果 NumOrSum 是None ,则默认按照个数统计，如果不是则按照求和统计
                    if self.SumItem == None:
                        # 求个数
                        data_list.append(data.id.count())
                    else:
                        #     求其他字段的和
                        # 将字段的空置处理成0
                        data[self.SumItem] = data[self.SumItem].fillna(value=0)
                        # 将字段中可能存在的非数字转为0
                        data[self.SumItem] = data[self.SumItem].apply(lambda x: int(x) if str(x).isdecimal() else 0)
                        # print(data['user_pv'])
                        data_list.append(data[self.SumItem].sum())

                # 使用字典模式生成新的df
                cal_data = {
                    self.args: name_list,
                    'data': data_list
                }

                cal_df = pd.DataFrame(cal_data)
                # print(cal_df)

                # 处理成从小到大排列的数据
                cal_df = cal_df.sort_values(by=['data'], ascending=False)
                return cal_df
        else:
            return self.df

    def getTopNum(self):
        cal_df = self.GroupDate()
        if isinstance(cal_df,pd.DataFrame):
            if len(cal_df) > self.top_num:
                # 排名前几名的数据
                df_top = cal_df.iloc[:self.top_num]
                # print(df_top)
                # 除去排名前几的其他数据统计为"其他"
                df_others = cal_df.iloc[self.top_num:]
                df_other_sum = df_others['data'].sum()
                # print(df_other_sum)
                df_top_app = pd.DataFrame({self.args: '其他分类之和', 'data': df_other_sum}, index=[1])
                # print(df_top_app)
                df_top_new = df_top.append(df_top_app, ignore_index=False)

            else:
                df_top_new = cal_df
            # 计算每个值的占比
            all_num = cal_df['data'].sum()
            df_top_new['占比'] = df_top_new['data'] / all_num
            # 转为百分制显示
            df_top_new['占比'] = df_top_new['占比'].apply(lambda x: format(x, '.2%'))
            writeToExcelFile(df_top_new, str(self.args)[2:-3])
            return df_top_new
        else:
            return cal_df

    def showPie(self, save_name):
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 处理中文
        plt.title('按照"{}"分类查看'.format(str(self.args)[2:-3]))
        df_top_new = self.getTopNum()
        # print(df_top_new)
        # 判断是否有数据
        if isinstance(df_top_new,pd.DataFrame):
            try:
                plt.pie(df_top_new['data'], labels=df_top_new[self.args], autopct='%.1f%%', startangle=90,
                        wedgeprops={'linewidth': 50}, counterclock=False)
                pic_name = get_dir(save_name, str(self.args)[2:-3] + '.png')
                plt.savefig(pic_name)

                plt.show()
            except Exception as e:
                print(e)
        else:
            print(df_top_new)


if __name__ == '__main__':
    new_df = CalDataToShow('用户痛点吐槽_result_20211017.xlsx', 'Sheet1', 8, None, 'belongs')
    # df_top_new = new_df.getTopNum()
    new_df.showPie('results_file/UserPortraitPic')
