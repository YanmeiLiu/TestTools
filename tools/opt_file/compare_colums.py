"""
比较excel表中A列中的数据是否存在于B列中
"""
import pandas as pd
from TestTools.config.setconfig import get_dir
from TestTools.tools.opt_file.optFiles import CompareColums, ReadFileAsDF, writeToExcelFile

file_1 = get_dir('data_files/user_event', '商家端登录.xlsx')
df = ReadFileAsDF(file_1, sheet_name='1')
if isinstance(df, pd.DataFrame):
    new_df = CompareColums(df, 'busi_mobile', 'mobile')
    if isinstance(new_df, pd.DataFrame):
        writeToExcelFile(new_df, file_1, sheet_name='result')
    else:
        print(new_df)
else:
    print(df)
