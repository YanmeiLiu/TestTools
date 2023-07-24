from TestTools.config.setconfig import get_dir

from TestTools.tools.opt_file.optFiles import ReadFileAsDF, ConversionBigNum, writeToExcelFile

filename = 'query-impala-92135.csv'
file_name = get_dir('data_files/user_event', filename)

df = ReadFileAsDF(file_name)
new_df = ConversionBigNum(df, 'user_id')
writeToExcelFile(new_df, file_name, sheet_name='sheet')
