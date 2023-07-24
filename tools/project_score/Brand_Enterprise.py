from TestTools.config.db import Mysql
import time
import datetime
import re
from decimal import Decimal


# 产品所在公司的成立年数,行业，是否国际化
# 品牌力-营收状况-业务成立时长
# 品牌力-市场广度-多行业、国际化
class Enterprise(object):
    def getEnterprise(self,project_id):
        sql = "select founded_at,industry,has_overseas from enterprise where id = (select ent_id from project where id = %d);" % project_id
        sql_result = Mysql('yellowPageDB').select(sql)
        # print(sql_result,type(sql_result))
        if sql_result:
            # 判断founded_at
            if sql_result[0][0] == '' or sql_result[0][0] == None or sql_result[0][0] == '0000-00-00 00:00:00':
                already_found = -1
            else:
                #     计算成立时间
                ent_year = str(sql_result[0][0]).split('-')[0]
                #     获取当前年份
                current_year = datetime.datetime.now().year
                already_found = int(current_year) - int(ent_year)
            #   判断industry
            if sql_result[0][1] != '':
                # 按照,分割
                industry = sql_result[0][1]
                industry_num = len(industry.split(','))
            else:
                industry = ''
                industry_num = 0
            #     判断has_overseas
            if sql_result[0][2] == 1:  # 表示国际
                overseas = 1
                print('project_id = {} 的公司是国际化企业'.format(project_id))

            elif sql_result[0][2] == 0:
                overseas = 0
                print('project_id = {} 的公司不是国际化企业'.format(project_id))
            else:
                overseas = 0
                print('project_id = {} 的公司不是国际化企业'.format(project_id))

            print('project_id = {} 的公司已经成立{}年,涉及 {} 个行业'.format(project_id, already_found, industry_num))
        else:
            print('project_id = {}所在的企业不存在'.format(project_id))
            already_found = -1
            industry = ''
            industry_num = -1
            overseas = -1

        return already_found, industry, industry_num, overseas

    def getAllEnterprise(self):
        sql = "select id from project where state= 1 and source = 1;"
        sql_result = Mysql('yellowPageDB').select(sql)
        for i in sql_result:
            project_id = i[0]
            already_found, industry, industry_num, overseas = self.getEnterprise(project_id)

            # 本地数据库插入数据
            # 当前时间
            created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            sql_insert = "INSERT INTO `project_market_span_tmp`" \
                         " ( `project_id`, `industry`, `industry_num`, `has_overseas`, `already_found`, `created_at`)" \
                         " VALUES(%d,'%s',%d,%d,%d,'%s');" % (
                             project_id, industry, industry_num, overseas, already_found, created_at)
            print(sql_insert)
            Mysql('localhost').insert(sql_insert)

    def MaxAndMinFound(self):
        sql = "select max(already_found) ,min(already_found) from project_market_span_tmp where already_found>=0 ;"
        sql_result = Mysql('localhost').select(sql)
        found_max = sql_result[0][0]
        found_min = sql_result[0][1]
        return found_max, found_min

    def MaxAndMinIndustry(self):
        sql = "select max(industry_num) ,min(industry_num) from project_market_span_tmp where industry_num>=0 ;"
        sql_result = Mysql('localhost').select(sql)
        industry_max = sql_result[0][0]
        industry_min = sql_result[0][1]
        return industry_max, industry_min

    def NormalFoundAndIndustry(self):
        self.getAllEnterprise()
        industry_max, industry_min = self.MaxAndMinIndustry()
        found_max, found_min = self.MaxAndMinFound()
        # 处理轮次和amount
        sql = "select project_id ,industry_num,has_overseas,already_found from project_market_span_tmp;;"
        sql_result = Mysql('localhost').select(sql)
        for i in sql_result:
            if i[1] <= 0:
                industry_score = 0
            else:
                industry_score = Decimal(i[1] - industry_min) / (industry_max - industry_min)
            if i[2] == 0:
                overseas_score = 0
            else:
                overseas_score = 1
            if i[3] <= 0:
                found_score = 0
            else:
                found_score = Decimal(i[3] - found_min) / (found_max - found_min)

            # 当前时间
            created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            sql_insert = "INSERT INTO `project_market_score`" \
                         " ( `project_id`, `found_num`, `found_max`, `found_min`, `found_score`, " \
                         "`industry_num`, `industry_max`, `industry_min`, `industry_score`, `overseas`,`overseas_score`,`created_at`) " \
                         "VALUES(%d,%d,%d,%d,%s,%d,%d,%d,%s,%d,%s,'%s'); " % (
                             i[0], i[3], found_max, found_min, found_score, i[1], industry_max, industry_min,
                             industry_score, i[2], overseas_score, created_at)
            print(sql_insert)
            Mysql('localhost').insert(sql_insert)


if __name__ == '__main__':
    mm = Enterprise()
    mm.NormalFoundAndIndustry()
