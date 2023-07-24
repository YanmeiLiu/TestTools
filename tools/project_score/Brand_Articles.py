from TestTools.config.db import Mysql
import time
import datetime
import re
from decimal import Decimal


class Articles(object):

    # 品牌力中的 -品牌热度-平台指数-产品引用文章数
    # 有关联的文章数
    def getArticle(self, project_id):
        sql = "select count(distinct(product_evaluation_id)) from product_evaluation_related " \
              "where project_id = %d " \
              "and product_evaluation_id in (select id from product_evaluation where  state=1);" % project_id
        sql_result = Mysql('yellowPageDB').select(sql)
        article_num = sql_result[0][0]
        print('project_id = {}关联了{}篇文章'.format(project_id, article_num))
        return project_id, article_num

    def getAllArticle(self):
        sql = "select id from project where state =1 and source = 1;"
        sql_result = Mysql('yellowPageDB').select(sql)
        for i in sql_result:
            project_id = i[0]
            project_id, article_num = self.getArticle(project_id)
            # 当前时间
            created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            sql_insert = "INSERT INTO `project_articel_score` ( `project_id`, `article_num`,  `created_at`)" \
                         " VALUES(%d,%d,'%s');" % (
                             project_id, article_num, created_at)
            print(sql_insert)
            Mysql('localhost').insert(sql_insert)

    def MaxAndMinArticle(self):
        sql = "select max(article_num) ,min(article_num) from project_articel_score ;"
        sql_result = Mysql('localhost').select(sql)
        article_max = sql_result[0][0]
        article_min = sql_result[0][1]
        return article_max, article_min

    def NormalArticle(self):
        self.getAllArticle()
        article_max, article_min = self.MaxAndMinArticle()
        sql = "select id,project_id,article_num from project_articel_score  ;"
        sql_result = Mysql('localhost').select(sql)
        for i in sql_result:
            if i[2] == 0:
                article_score = 0
            else:
                article_score = Decimal(i[2] - article_min) / (article_max - article_min)
            # 当前时间
            updated_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            sql_update = "update  `project_articel_score` set article_score = '%s',article_max='%s',article_min='%s',updated_at ='%s'" \
                         " where id = %d " % (
                             article_score, article_max, article_min, updated_at, i[0])
            print(sql_update)
            Mysql('localhost').update(sql_update)


if __name__ == '__main__':
    mm = Articles()
    mm.NormalArticle()
