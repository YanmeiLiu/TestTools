
# 使用csv读取
from config.setconfig import get_dir
from tools.opt_file.optFiles import ReadFileAsDF, writeToExcelFile

filename = 'users.xlsx'
file_name = get_dir('data_files/user_event', filename)

df = ReadFileAsDF(file_name,sheet_name='SheetJS')
print(df.columns)

# 替换文件中内容
df['related_id'].replace([1, 2, 3, 4, 5],
                         ['VIP会员-连续包月首季度每月1元', 'VIP会员-连续包月', 'VIP会员-年缴', 'VIP会员-连续包月首月1元', 'VIP会员-年缴赠6个月'],
                         inplace=True)
df['goods_id'].replace([1, 2, 3, 4, 5],
                       ['VIP会员-连续包月首季度每月1元', 'VIP会员-连续包月', 'VIP会员-年缴', 'VIP会员-连续包月首月1元', 'VIP会员-年缴赠6个月'],
                       inplace=True)
# df['state'].replace([0, 1, 2, 3, 4], ['未支付', '已支付', '已过期', '部分退款', '全部已退款'], inplace=True)
df['state'].replace([0, 1, 2, 3], ['初始状态', '生效中', '已失效', '已续费'], inplace=True)
df['pay_duration'].replace([1, 2, 3], ['月缴', '季缴', '年缴'], inplace=True)
# df['pay_type'].replace([0, 1, 2], ['未知', '微信', '支付宝'], inplace=True)
# df['order_type'].replace([0, 1], ['手动支付', '自动代扣'], inplace=True)

# 替换文件头
df = df.rename(
    columns={'real_name': '真实姓名', 'mobile': '手机号', 'user_state': '当前状态', 'pay_duration': '缴费方式',
             'order_state': '账单状态', 'begin_at': '会员开始时间', 'end_at': '会员截止时间',
             'bill_amount': '实际支付金额（分）', 'pay_type': '支付方式', 'refund_amount': '已退款金额', 'order_type': '订单类型',
             'created_at': '订单创建时间', 'related_id': '会员购买套餐', 'goods_id': '订单中购买套餐', 'id': 'user_id'})
# 输出文件
writeToExcelFile(df, file_name, sheet_name='sheet')

