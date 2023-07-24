# 更新index_spider表的数据
import datetime, time
import random

from config.db import Mysql
from tools.get_day_time import GetDateTime


class updateData(object):
    def __init__(self):
        self.current_date = time.strftime("%Y-%m-%d", time.localtime())
        get_day = GetDateTime(self.current_date, days=-7)
        self.that_date = get_day.getDate()

    # 将created_at时间 更新到 spider_date
    def updateSpiderByCreated(self):
        sql_update = " update index_spider set spider_date = date(created_at);"
        print(sql_update)
        Mysql('yellowPageDB').update(sql_update)

    # 将数据表中的spider_date更新为最近7天
    def updateIndexSpiderDate(self):
        """
        根据project 表中 state = 1的数据更新
        获取当前的时间，然后在当前时间下递减1天，直到7天前，还要注意已经修改后的要剔除出去

        :return:
        """
        # 先将不在这个区间的数据过滤出所有的product_id
        sql = "select distinct(product_id) from index_spider " \
              "where (spider_date  <'%s' or spider_date  >'%s') " \
              "and product_id in (select id from project where state =1 );" % (
                  self.that_date, self.current_date)
        print(sql)
        sql_result = Mysql('yellowPageDB').select(sql)
        for nu in range(0, -7, -1):
            for i in sql_result:
                sql_select = "select max(id) from  index_spider where product_id =%d " \
                             "and (spider_date  <'%s' or spider_date  >'%s') ;" % \
                             (i[0], self.that_date, self.current_date)
                print(sql_select)
                sql_select_result = Mysql('yellowPageDB').select(sql_select)
                if sql_select_result[0][0] is not None:
                    get_spider_date = GetDateTime(self.current_date, days=nu)
                    spider_date = str(get_spider_date.getDate())[0:10]

                    sql_update = " update index_spider set spider_date = '%s' where id = '%s';" % \
                                 (spider_date, sql_select_result[0][0])
                    print(sql_update)
                    Mysql('yellowPageDB').update(sql_update)

    # 将表中数据为0的数据随机赋值
    # 数据中存在字段都是0的可能性比较大，所以还要更新每个字段随机赋值
    def updateIndexSpiderNum(self):
        # 过滤该时间区间内的数据为0 的
        sql = "select id from index_spider " \
              "where (spider_date  >='%s' and spider_date  <='%s') " \
              "and (baidu_index=0 or toutiao_index=0 or sougou_index=0 " \
              "or weixin_articles_num=0 or zhihu_articles_num=0 or baidu_search_num=0 or baidu_include_num=0);" % (
                  self.that_date, self.current_date)
        print(sql)
        sql_result = Mysql('yellowPageDB').select(sql)
        if sql_result is not None:
            for i in sql_result:
                sql_update = " update index_spider set baidu_index=%d," \
                             "toutiao_index=%d," \
                             "sougou_index=%d," \
                             "weixin_articles_num=%d," \
                             "zhihu_articles_num=%d," \
                             "baidu_search_num=%d," \
                             "baidu_include_num=%d where id = '%s';" % \
                             (random.randint(0, 100), random.randint(0, 100),
                              random.randint(0, 100), random.randint(0, 100),
                              random.randint(0, 100), random.randint(0, 100),
                              random.randint(0, 100), i[0])
                print(sql_update)
                Mysql('yellowPageDB').update(sql_update)


if __name__ == '__main__':
    ud = updateData()
    ud.updateIndexSpiderNum()
    # updateSpiderByCreated()
