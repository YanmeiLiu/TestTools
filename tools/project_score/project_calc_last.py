#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 计算企服点评平台产品评分
# user : liuyanmei
# date :2021-1-15
# updated_at :2021-2-8 ，当前已经是第二次改版后的结果

import re
import time
import datetime

from config.db import Mysql
from decimal import Decimal

from get_day_time import GetDateTime


class LastScore(object):
    def __init__(self):
        self.current_date = time.strftime("%Y-%m-%d", time.localtime())
        get_day = GetDateTime(self.current_date, days=-7)
        self.that_date = get_day.getDate()

    # 计算最后
    def calLast(self, project_id):
        # 计算最后的用户评分40%
        sql = "select final_user_score from project_user_score_final where project_id = %d;" % project_id
        sql_result = Mysql('localhost').select(sql)
        if sql_result:
            final_user_score = float(sql_result[0][0])
            user_score = final_user_score * 40 / 100
        else:
            user_score = 0
        # 计算最后的企业信息质量30%，信息完善度 25%
        sql_info = "select normal_score,firm_score,operate_score " \
                   "from project_info_score where project_id = %d and date(updated_at)='%s' limit 1;" % (
                       project_id, self.current_date)
        sql_info_result = Mysql('localhost').select(sql_info)
        print(sql_info)
        if sql_info_result:
            normal_score = float(sql_info_result[0][0])
            firm_score = float(sql_info_result[0][1])
            if sql_info_result[0][2] is None:
                operate_score = 0
            else:

                operate_score = float(sql_info_result[0][2])
            info_score = normal_score * 25 / 100 + (
                    firm_score + operate_score) * 2.5 / 100
        else:
            info_score = 0

        #     计算品牌力得分
        #     营收状况
        sql_amount = "select round_score, amount_score,ipo_score from project_round_score where project_id = %d;" % project_id
        sql_amount_result = Mysql('localhost').select(sql_amount)
        if sql_amount_result:
            round_score = float(sql_amount_result[0][0])
            amount_score = float(sql_amount_result[0][1])
            ipo_score = float(sql_amount_result[0][2])
            if sql_amount_result[0][2] > 0:
                is_ipo = ipo_score * 1 / 100
            else:
                is_ipo = (amount_score + round_score) * 0.5 / 100
        else:
            is_ipo = 0

        sql_industry = "select found_score,industry_score,overseas_score from project_market_score where project_id = %d;" % project_id
        sql_industry_result = Mysql('localhost').select(sql_industry)
        if sql_industry_result:
            found_score = float(sql_industry_result[0][0])
            industry_score = float(sql_industry_result[0][1])
            overseas_score = float(sql_industry_result[0][2])
            found_score = found_score * 0.5 / 100
            industry_score = industry_score * 1.25 / 100
            overseas_score = overseas_score * 1.25 / 100
        else:
            found_score = 0
            industry_score = 0
            overseas_score = 0
        #     引用文章数
        sql_article = "select article_score from project_articel_score where project_id = %d;" % project_id
        sql_article_result = Mysql('localhost').select(sql_article)
        if sql_article_result:
            article_score = float(sql_article_result[0][0])
            article_score = article_score * 5 / 100
        else:
            article_score = 0
        #    外部平台指数，百度，知乎，微信
        sql_out = "select baidu_score,weixin_score,zhihu_score,baidu_include_score from index_score where project_id = %d;" % project_id
        sql_out_result = Mysql('localhost').select(sql_out)
        if sql_out_result:
            baidu_score = float(sql_out_result[0][0])
            weixin_score = float(sql_out_result[0][1])
            zhihu_score = float(sql_out_result[0][2])
            baidu_include_score = float(sql_out_result[0][3])

            baidu_score = baidu_score * 5 / 100
            baidu_include_score = baidu_include_score * 25 / 1000

            weixin_score = weixin_score * 5 / 100
            zhihu_score = zhihu_score * 25 / 1000
        else:
            baidu_score = 0
            weixin_score = 0
            zhihu_score = 0
            baidu_include_score = 0

            #     第一轮，计算总分，缺少内部平台的分数
        # brand_score = (
        #                       baidu_score + weixin_score + zhihu_score) + article_score + is_ipo + found_score + industry_score + overseas_score
        # print('project_id = {} 的user_score{},\nbrand_score:{},\ninfo_score:{}'.format(project_id, user_score, brand_score,
        #                                                                               info_score))

        #     第二轮，计算总分，缺少内部平台的分数
        # 假设pv_finale_score= 0
        pv_finale_score = 0
        brand_score = (baidu_score + weixin_score + zhihu_score + baidu_include_score) + article_score + pv_finale_score
        print(
            'project_id = {} 的user_score{},\nbrand_score:{},\ninfo_score:{}'.format(project_id, user_score, brand_score,
                                                                                    info_score))
        return user_score, brand_score, info_score

    def getAllScore(self):
        sql = "select id from project where state =1 and source = 1;"
        sql_result = Mysql('yellowPageDB').select(sql)
        for i in sql_result:
            user_score, brand_score, info_score = self.calLast(int(i[0]))
            total_score = user_score + brand_score + info_score
            # 当前时间
            created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            sql_insert = "INSERT INTO `user_brand_info_score` ( `project_id`, `user_score`, `brand_heat_score`, `info_score`, `total_score`,`created_at`)" \
                         "VALUES(%d,%s,%s,%s,%s,'%s'); " % (
                             i[0], user_score, brand_score, info_score, total_score, created_at)
            print(sql_insert)
            Mysql('localhost').insert(sql_insert)


if __name__ == '__main__':
    mm = LastScore()
    mm.getAllScore()
