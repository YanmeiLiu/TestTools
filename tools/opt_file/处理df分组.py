from TestTools.config.setconfig import get_dir
from TestTools.tools.opt_file.optFiles import ReadFileAsDF, groupByItem, writeToExcelFile, MergetDF


def cutAndmerge(df, cut_df, merge_df, merge_type):  # 分割后按照一个字段再合并
    global new_df
    df_lists = groupByItem(df, cut_df)
    if df_lists:
        for dl in enumerate(df_lists):
            for k, v in dl[1].items():
                if dl[0] == 0:
                    new_df = v.copy()
                else:
                    new_df = MergetDF(new_df, v.copy(), merge_df, merge_type)
    writeToExcelFile(new_df, file_name, sheet_name='sheet')


def cutdf(df, cut_df):  # 分割后按照一个字段再合并
    df_lists = groupByItem(df, cut_df)
    if df_lists:
        for dl in df_lists:
            for k, v in dl.items():
                writeToExcelFile(v.copy(), file_name, sheet_name=str(k))


if __name__ == '__main__':
    file_name = get_dir('data_files/user_event', '查询站外搜索用户每日访问pv (1).xlsx')
    df = ReadFileAsDF(file_name, '1')
    cutAndmerge(df, '$os', ['page'], 'outer')
    # cutdf(df, '端')
