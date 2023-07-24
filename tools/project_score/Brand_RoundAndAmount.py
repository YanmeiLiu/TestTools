from TestTools.config.db import Mysql
import time
import datetime
import re
from decimal import Decimal


# 判断是否上市企业，融资金额
# 品牌力-营收状况-是否上市企业，融资金额
class RoundAndAmount(object):
    def ifInternatioal(self,project_id):
        sql = "select id,round,amount,state,project_id  from ent_financing  where project_id = %d;" % project_id
        sql_result = Mysql('yellowPageDB').select(sql)
        s = 0
        total_amount = 0
        financing_count = 0
        if sql_result == '' or sql_result == None:
            # 不是上市企业，也不是融资企业
            s = s
            total_amount = total_amount
            financing_count = financing_count
            print('该企业既不是上市企业，亦不是融资企业')

        else:
            s = 0
            total_amount = 0
            financing_count = 0
            for i in sql_result:
                # 判断round字段
                if i[1] in ['上市', '上市后', '新三板', '新四板', 'IPO', 'IPO上市']:
                    print('project_id = {}是上市公司'.format(project_id))
                    s = 1
                elif i[1] in ['种子轮', '天使轮', 'Pre-A轮', 'A轮', 'A+轮', 'B轮', 'B+轮', 'C轮', 'C+轮', 'D轮', 'D+轮', 'E轮', 'E+轮',
                              'F轮',
                              'F+轮', 'E轮及以后', 'Pre-B轮', '定向增发', '战略融资或战略投资', 'Pre-IPO', '股权融资', '战略融资']:
                    print('project_id = {}已融资但是未上市'.format(project_id))
                    s = s
                # 计算融资金额，amount
                # 正则匹配金额
                res_amount = re.search(r'([\d+\.]+)', i[2])
                financing_count += 1
                if res_amount:
                    if re.search('万', i[2]):
                        amount = Decimal(res_amount.group(0)) * 10000
                    elif re.search('亿', i[2]):
                        amount = Decimal(res_amount.group(0)) * 100000000
                    else:
                        amount = Decimal(res_amount.group(0))

                    if re.search('美元', i[2]):
                        rmb_amount = amount * 6
                    elif re.search('港元', i[2]):
                        rmb_amount = amount * Decimal(0.5)
                    else:
                        rmb_amount = amount

                    total_amount += rmb_amount
            print('该企业已融资{}轮，且融资金额是: {}人民币 '.format(financing_count, total_amount))
        return s, financing_count, total_amount

    # 计算所有企业的融资数额
    def calRound(self):
        sql = "select id from project where state =1 and source = 1;"
        sql_result = Mysql('yellowPageDB').select(sql)
        for i in sql_result:
            project_id = i[0]
            print(project_id)
            s, financing_count, total_amount = self.ifInternatioal(project_id)

            # 当前时间
            created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            sql_insert = "INSERT INTO `project_round` ( `project_id`, `amount`, `round`, `ipo`, `created_at`)" \
                         " VALUES(%d,%d,%d,%d,'%s');" % (
                             project_id, total_amount, financing_count, s, created_at)
            Mysql('localhost').insert(sql_insert)

    def MaxAndMinRound(self):
        sql = "select max(round) ,min(round) from project_round  ;"
        sql_result = Mysql('localhost').select(sql)
        round_max = sql_result[0][0]
        round_min = sql_result[0][1]
        return round_max, round_min

    def MaxAndMinAmount(self):
        sql = "select max(amount) ,min(amount) from project_round  ;"
        sql_result = Mysql('localhost').select(sql)
        amount_max = sql_result[0][0]
        amount_min = sql_result[0][1]
        return amount_max, amount_min

    # # 归一化融资轮次，金额
    def NormalRoundAndAmount(self):
        self.calRound()
        round_max, round_min = self.MaxAndMinRound()
        amount_max, amount_min = self.MaxAndMinAmount()
        # 处理轮次和amount
        sql = "select project_id,round,amount,ipo from project_round  ;"
        sql_result = Mysql('localhost').select(sql)
        for i in sql_result:
            if i[3] == 0:
                print(i[3])
                round_score = Decimal(i[1] - round_min) / (round_max - round_min)
                amount_score = Decimal(i[2] - amount_min) / (amount_max - amount_min)
                # 当前时间
                created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                sql_insert = "INSERT INTO `project_round_score` " \
                             "( `project_id`,`round`, `round_max`, `round_min`, `round_score`, `amount`, " \
                             "`amount_max`, `amount_min`, `amount_score`, `ipo_score`, `created_at`) VALUES(%d,%d,%d,%d,%s,%d,%d,%d,%s,%d,'%s'); " % (
                                 i[0], i[1], round_max, round_min, round_score, i[2], amount_max, amount_min,
                                 amount_score,
                                 0,
                                 created_at)
                print(sql_insert)
                Mysql('localhost').insert(sql_insert)
            else:
                # 当前时间
                created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                sql_insert = "INSERT INTO `project_round_score` " \
                             "( `project_id`,`round`, `round_max`, `round_min`, `round_score`, `amount`, " \
                             "`amount_max`, `amount_min`, `amount_score`, `ipo_score`, `created_at`) VALUES(%d,%d,%d,%d,%s,%d,%d,%d,%s,%d,'%s'); " % (
                                 i[0], 0, 0, 0, 0, 0, 0, 0, 0, 1,
                                 created_at)
                print(sql_insert)
                Mysql('localhost').insert(sql_insert)


if __name__ == '__main__':
    mm = RoundAndAmount()
    mm.NormalRoundAndAmount()
