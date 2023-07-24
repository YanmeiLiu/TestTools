
import pandas as pd

from TestTools.config.setconfig import get_dir
from TestTools.tools.opt_file.optFiles import ReadFileAsDF, ReplaceText, writeToExcelFile


# 主要用于判断project_count字段
def calItem(col1, col2):
    if col1 == 0 and col2 == 0:
        result = 0
    elif col1 == 0 and col2 != 0:
        result = 1
    else:
        result = col1
    return result


def calProject(df, *args):
    if df is not None:
        if args is None:
            return
        else:
            col_names = df.columns.tolist()  # 将数据框的列名全部提取出来存放在列表里
            # print(col_names)
            # 获取参数名
            group_cols = []
            # 形参是列表，将列表中的数据都拿出来看是否在df中存在，如果都存在则可以分组处理
            for group_col in args:
                if group_col in col_names:
                    group_cols.append(group_col)
                    # 将为空的值处理成未知
                    df[group_col] = df[group_col].fillna(value=0)
                else:
                    # break
                    raise NameError(" 存在参数名错误.")
            # 分组 计算project_count
            new_df = df.groupby(group_cols)
            name_list = []
            data_list = []
            # 创建一个与df相同的空df
            last_df = pd.DataFrame(index=df.index, columns=df.columns)
            for name, data in new_df:
                name_list.append(name)
                # 将为空的值处理成0
                data['project_name'] = data['project_name'].fillna(value=0)
                # print(data['project_count'], data['project_name'])

                """
                判断data['project_name']为空则 data['project_count'] 仍旧是0 
                 若 data['project_name'] 有值，则 data['project_count'] 为1
                """
                data['result'] = list(map(lambda x, y: calItem(x, y), data['project_count'], data['project_name']))

                # 求个数
                # 如果个数大于1，则需要处理，如果个数=1 ，则不需要处理
                if data.id.count() > 1:
                    # 求project_count之和
                    data['project_count'] = data['project_count'].apply(lambda x: int(x) if str(x).isdecimal() else 0)
                    # print(data['user_pv'])
                    data_list.append(data['result'].sum())
                    #
                    data['sum'] = data['result'].sum()
                    #     根据user_id去重
                    data.drop_duplicates(subset=['new_user_id'], keep='first', inplace=True)

                else:
                    data_list.append(data['result'])
                    data['sum'] = data['result']
                # 将data合并到一个整体的结果中
                last_df = pd.concat([last_df, data], axis=0)
            # 删除time为空的行
            last_df = last_df.dropna(subset=["time"])
            return last_df
    else:
        return


if __name__ == '__main__':
    filename = '处理后的神策ID.xlsx'
    file_name = get_dir('data_files', filename)
    df = ReadFileAsDF(file_name, sheet_name='sheet2')
    last_df = calProject(df, 'new_user_id')
    new_df = ReplaceText(last_df, 'filename', 'getinfo_button')
    writeToExcelFile(last_df, file_name, sheet_name='sheet')
