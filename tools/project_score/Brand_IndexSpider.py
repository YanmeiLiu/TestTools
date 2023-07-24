from TestTools.config.db import Mysql
import time
import datetime
import re
from decimal import Decimal


# 获取当前product_id的最近7天的平均值
# 品牌力-品牌热度-外部指数
class OutsideIndex(object):
    def __init__(self):
        # 获取当前日期
        current_day = datetime.datetime.now()
        days = datetime.timedelta(days=7)
        start_date = current_day - days
        start_date_to = datetime.datetime(start_date.year, start_date.month, start_date.day)
        end_date_to = datetime.datetime(current_day.year, current_day.month, current_day.day)

        self.end_date = str(end_date_to)[0:10]
        self.start_date = str(start_date_to)[0:10]
        # print('从{}开始获取'.format(start_date))

    def getIndexSpider(self, project_id, project_name, project_website):
        sql = "select  product_id,product_name,website,baidu_search_num,weixin_articles_num,zhihu_articles_num,baidu_include_num " \
              "from index_spider where product_id =%d and spider_date >='%s'  and spider_date<'%s' order by id desc ;" % (
                  project_id, self.start_date, self.end_date)
        print(sql)
        sql_result = Mysql('yellowPageDB').select(sql)

        baidu = 0
        weixin = 0
        zhihu = 0
        baidu_include = 0

        baidu_num = 0
        weixin_num = 0
        zhihu_num = 0
        baidu_include_num = 0
        if sql_result:
            for i in sql_result:
                if i[1] == project_name and i[2] == project_website:
                    if int(i[3]) != 0:
                        baidu += int(i[3])
                        baidu_num += 1
                    if int(i[4]) != 0:
                        weixin += int(i[4])
                        weixin_num += 1
                    if int(i[5]) != 0:
                        zhihu += int(i[5])
                        zhihu_num += 1
                    if int(i[6]) != 0:
                        baidu_include += int(i[6])
                        baidu_include_num += 1
                else:
                    break
            if baidu_num != 0:
                baidu_avg = baidu / baidu_num
            else:
                baidu_avg = 0
            if weixin_num != 0:
                weixin_avg = weixin / weixin_num
            else:
                weixin_avg = 0
            if zhihu_num != 0:
                zhihu_avg = zhihu / zhihu_num
            else:
                zhihu_avg = 0
            if baidu_include_num != 0:
                baidu_include_avg = baidu_include / baidu_include_num
            else:
                baidu_include_avg = 0
        else:
            baidu_avg = 0
            weixin_avg = 0
            zhihu_avg = 0
            baidu_include_avg = 0

        return baidu, baidu_num, baidu_avg, \
               baidu_include, baidu_include_num, baidu_include_avg, \
               weixin, weixin_num, weixin_avg, \
               zhihu, zhihu_num, zhihu_avg

    def getAllIndexSpider(self):
        sql = "select id,name,website from project where state =1 and source = 1;"
        sql_result = Mysql('yellowPageDB').select(sql)
        for i in sql_result:
            baidu, baidu_num, baidu_avg, \
            baidu_include, baidu_include_num, baidu_include_avg, \
            weixin, weixin_num, weixin_avg, \
            zhihu, zhihu_num, zhihu_avg = self.getIndexSpider(i[0], i[1], i[2])
            # 当前时间
            created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            sql_insert = "INSERT INTO `index_7days_avg` ( `project_id`,`baidu_total`,`baidu_num`, `baidu_avg`," \
                         "`weixin_total`,`weixin_num`,`weixin_avg`," \
                         "`zhihu_total`,`zhihu_num`,`zhihu_avg`, " \
                         "`baidu_include_total`,`baidu_include_num`,`baidu_include_avg`, " \
                         " `created_at`)" \
                         " VALUES(%d,%d,%d,%s,%d,%d,%s,%d,%d,%s,%d,%d,%s,'%s');" % (
                             i[0], baidu, baidu_num, baidu_avg, weixin, weixin_num, weixin_avg, zhihu, zhihu_num,
                             zhihu_avg,
                             baidu_include, baidu_include_num, baidu_include_avg,
                             created_at)
            print(sql_insert)
            Mysql('localhost').insert(sql_insert)

    def MaxAndMinSpider(self):
        sql = "select max(baidu_avg) ,min(baidu_avg),max(weixin_avg) ,min(weixin_avg), max(zhihu_avg) ,min(zhihu_avg) ,max(baidu_include_avg) ,min(baidu_include_avg)  from index_7days_avg  ;"
        sql_result = Mysql('localhost').select(sql)
        baidu_avg_max = sql_result[0][0]
        baidu_avg_min = sql_result[0][1]
        weixin_avg_max = sql_result[0][2]
        weixin_avg_min = sql_result[0][3]
        zhihu_avg_max = sql_result[0][4]
        zhihu_avg_min = sql_result[0][5]
        baidu_include_avg_max = sql_result[0][6]
        baidu_include_avg_min = sql_result[0][7]
        return baidu_avg_max, baidu_avg_min, weixin_avg_max, weixin_avg_min, zhihu_avg_max, zhihu_avg_min, baidu_include_avg_max, baidu_include_avg_min

    # 归一化
    def NormalSpider(self):
        self.getAllIndexSpider()
        baidu_avg_max, baidu_avg_min, \
        weixin_avg_max, weixin_avg_min, \
        zhihu_avg_max, zhihu_avg_min, \
        baidu_include_avg_max, baidu_include_avg_min = self.MaxAndMinSpider()

        sql = "select project_id,baidu_avg,weixin_avg,zhihu_avg,baidu_include_avg from index_7days_avg  ;"
        sql_result = Mysql('localhost').select(sql)

        for i in sql_result:
            if baidu_avg_max == 0:
                final_baidu_score = 0
            else:
                final_baidu_score = Decimal(i[1] - baidu_avg_min) / Decimal(baidu_avg_max - baidu_avg_min)

            if weixin_avg_max == 0:
                final_weixin_score = 0
            else:
                final_weixin_score = Decimal(i[2] - weixin_avg_min) / Decimal(weixin_avg_max - weixin_avg_min)

            if zhihu_avg_max == 0:
                final_zhihu_score = 0
            else:
                final_zhihu_score = Decimal(i[3] - zhihu_avg_min) / Decimal(zhihu_avg_max - zhihu_avg_min)

            if baidu_include_avg_max == 0:
                final_baidu_include_score = 0
            else:
                final_baidu_include_score = Decimal(i[4] - baidu_include_avg_min) / Decimal(
                    baidu_include_avg_max - baidu_include_avg_min)

            # 当前时间
            created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            sql_insert = "INSERT INTO `index_score` ( `project_id`, `baidu_max`, `baidu_min`, `baidu_avg`, `baidu_score`," \
                         " `weixin_max`, `weixin_min`, `weixin_avg`, `weixin_score`, " \
                         "`zhihu_max`, `zhihu_min`, `zhihu_avg`, `zhihu_score`," \
                         "`baidu_include_max`, `baidu_include_min`, `baidu_include_avg`, `baidu_include_score`, `created_at`)" \
                         "VALUES(%d,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s'); " % (
                             i[0], baidu_avg_max, baidu_avg_min, i[1], final_baidu_score,
                             weixin_avg_max, weixin_avg_min, i[2], final_weixin_score,
                             zhihu_avg_max, zhihu_avg_min, i[3], final_zhihu_score,
                             baidu_include_avg_max, baidu_include_avg_min, i[4], final_baidu_include_score,
                             created_at)
            print(sql_insert)
            Mysql('localhost').insert(sql_insert)


if __name__ == '__main__':
    mm = OutsideIndex()
    mm.NormalSpider()
