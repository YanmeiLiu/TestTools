
from TestTools.config.setconfig import get_dir
from TestTools.tools.compile_projectid.dianping_crypto import encode_id, decode_id
from TestTools.tools.opt_file.optFiles import ReadFileAsDF, writeToExcelFile

file_name = get_dir('data_files/user_event', '页面点击_访问时长 (1).xlsx')

# df = ReadFileAsDF(file_name, sheet_name='sheet5')
# # df['encode_id'] = df['value'].apply(lambda x: encode_id(int(x)))
# # df['产品详情页链接'] = df['encode_id'].apply(lambda x: 'https://www.36dianping.com/space/' + str(x) + '')
# # df['问答资讯链接'] = df['encode_id'].apply(lambda x: 'https://www.36dianping.com/space/qa/' + str(x) + '/')
# df['取软件分类列表链接'] = df['value'].apply(lambda x: 'https://www.36dianping.com/brand/' + str(x) )

# 匹配出wensite中 带?和。的产品并标记出来
# df['web_if_param'] = df['website'].apply(lambda x: 'yes' if re.search('\\?|。', str(x)) else 'no')
# print(df['URL'])
# writeToExcelFile(df, file_name, sheet_name='sheet')
# 将url中的space_id转为实际的id
df = ReadFileAsDF(file_name, sheet_name='1')
df['decode_id'] = df['dianping_id'].apply(lambda x: decode_id(int(x)))
writeToExcelFile(df, file_name, sheet_name='sheet')
