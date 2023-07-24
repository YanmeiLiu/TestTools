#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 计算企服点评平台产品评分
# user : liuyanmei
# date :2021-10-11
# 2021.10.11新版本查看某一企业的信息完善度
# 需求地址：https://lop82is3mq.feishu.cn/docs/doccnFBuOMdEJWvZojfnZ7UDOxb
import re
import time
import datetime

from config.db import Mysql
from decimal import Decimal

# 计算产品的信息完善度
from tools.get_day_time import GetDateTime


class ProjecctInfoScore(object):
    def __init__(self):
        self.current_date = time.strftime("%Y-%m-%d", time.localtime())
        get_day = GetDateTime(self.current_date, days=-7)
        self.that_date = get_day.getDate()

    """
          分5部分计算：1、产品基础信息；2、行业案例；3、产品功能；4、产品价格；5、点评
          :param project_id:
          :return:
    """

    def getProjectBaseScore(self, project_id):
        # 初始化 产品基础信息 base_score
        base_score = 0
        # 获取产品
        sql_project = "select id,description,website from project where id = %d ;" % project_id
        sql_project_result = Mysql('yellowPageDB').select(sql_project)
        #     查询产品基础信息，在project,ent_product,enterprise,ent_product_attr表中
        # 如果产品存在，则有以下操作，如果不存在，则都为0
        if sql_project_result[0][0] > 0:
            description = sql_project_result[0][1]
            website = sql_project_result[0][2]
            print(description)
            # 一句话描述
            oneSentence_score = 0
            if description is not None and description != '':
                oneSentence_score = 3
            # 官网地址
            website_score = 0
            if website is not None and website != '':
                website_score = 1
            # enterprise公司信息
            sql_enterprise = "select id,full_name,date(founded_at),latest_financing,address from enterprise " \
                             "where id = (select ent_id from project where id = %d) ;" % project_id
            sql_enterprise_result = Mysql('yellowPageDB').select(sql_enterprise)
            full_name_score = founded_at_score = latest_financing_score = address_score = 0
            # 判断查询结果
            if sql_enterprise_result is not None:
                if sql_enterprise_result[0][0] > 0:
                    full_name = sql_enterprise_result[0][1]
                    founded_at = sql_enterprise_result[0][2]
                    latest_financing = sql_enterprise_result[0][3]
                    address = sql_enterprise_result[0][4]
                    # 公司名称是1分
                    if full_name is not None and full_name != '':
                        full_name_score = 1
                    # 公司成立时间是1分
                    if founded_at is not None and founded_at != '0000-00-00':
                        founded_at_score = 1
                    # 当前融资金额是1分
                    if latest_financing is not None and latest_financing != '':
                        latest_financing_score = 1
                    if address is not None and address != '':
                        address_score = 1
            else:
                print('该产品没有公司信息')
                full_name_score = full_name_score
                founded_at_score = founded_at_score
                latest_financing_score = latest_financing_score
                address_score = address_score
                print('enterprise表中有数据')

            # ent_product 产品信息介绍
            sql_product = "select description from ent_product " \
                          "where project_id   = %d  and state =0 and source = 1 ;" % project_id
            sql_product_result = Mysql('yellowPageDB').select(sql_product)
            # print(sql_product_result)
            # 查询结果为空
            if sql_product_result is not None:
                if sql_product_result[0][0] is not None:
                    project_description_score = 8
                else:
                    project_description_score = 0
            else:
                project_description_score = 0
                print('该产品不存在产品信息介绍')
            # ent_product_attr 产品截图
            sql_product_attr = "select count(*) from ent_product_attr " \
                               "where ent_product_id  = (select max(id) from ent_product where project_id = %d and source = 1) " \
                               "and category = 0 and state =0  ;" % project_id
            sql_product_attr_result = Mysql('yellowPageDB').select(sql_product_attr)
            project_pics_score = 0
            if sql_product_attr_result[0][0] > 0:
                project_pics_score = 2
            # ent_award 获奖信息
            sql_award = "select count(*) from ent_award  " \
                        "where project_id = %d and state =0  ;" % project_id
            sql_award_result = Mysql('yellowPageDB').select(sql_award)
            award_score = 0
            if sql_award_result[0][0] > 0:
                award_score = 2
            #     计算产品基础信息总分
            base_score = oneSentence_score + website_score + \
                         full_name_score + founded_at_score + \
                         latest_financing_score + address_score + \
                         project_description_score + project_pics_score + award_score
            print('oneSentence_score:{}, \n project_description_score:{},\n full_name_score :{},\n'
                  ' website_score:{} ，founded_at_score:{} ,\nlatest_financing_score:{} ,\n address_score:{} ,\n'
                  'project_pics_score :{}, \naward_score:{}\n'.format(
                oneSentence_score, project_description_score,
                full_name_score, website_score, founded_at_score,
                latest_financing_score, address_score,
                project_pics_score, award_score))
        else:
            base_score = base_score

        return base_score

    def getProjectCaseScore(self, project_id):
        # 初始化 行业案例 case_score = 行业案例 + 合作品牌
        # 获取行业案例个数
        sql_case = "select count(1) from ent_case where project_id = %d  and state = 0;" % project_id
        sql_case_result = Mysql('yellowPageDB').select(sql_case)
        case_score = 0
        case_count = sql_case_result[0][0]
        if case_count == 0:
            case_score = case_score
        elif case_count == 1:
            case_score = 2
        elif case_count == 2:
            case_score = 4
        elif case_count == 3:
            case_score = 7
        elif case_count == 4:
            case_score = 10
        elif case_count == 5:
            case_score = 13
        elif case_count == 6:
            case_score = 16
        elif case_count == 7:
            case_score = 20
        else:
            case_score = 20
        # 获取合作品牌个数
        sql_partner = "select count(1) from ent_partner where project_id = %d  and state = 0;" % project_id
        sql_partner_result = Mysql('yellowPageDB').select(sql_partner)
        partner_score = 0
        partner_count = sql_partner_result[0][0]
        if partner_count == 0:
            partner_score = partner_score
        elif 1 <= partner_count <= 3:
            partner_score = 3
        elif partner_count > 3:
            partner_score = 5
        else:
            partner_score = 5
        # 合并总分数
        case_partner_score = case_score + partner_score
        print('case_score:{},case_partner_score:{}'.format(case_score,case_partner_score))
        return case_partner_score

    def getProjectFunctionScore(self, project_id):
        # 初始化 产品功能 function_score
        # 分被认领的和不被认领的产品，下面的代码只是认领的产品，不考虑不被认领的
        # 获取行业案例个数
        sql_func = "select count(1) from business_project_func where project_id = %d  and state = 0 and parent_func_id!=0;" % project_id
        sql_func_result = Mysql('yellowPageDB').select(sql_func)
        function_score = 0
        func_count = sql_func_result[0][0]
        # print(func_count)
        if func_count > 0:
            function_score = 5
        print('function_score:', function_score)
        return function_score

    def getProjectPriceScore(self, project_id):
        # 产品价格 price_score  =  套餐 + 详细报单
        # 获取产品套餐
        sql_price_package = "select count(1) from project_price_detail where project_id = %d  and state = 0 ;" % project_id
        sql_pricce_package_result = Mysql('yellowPageDB').select(sql_price_package)
        price_count = sql_pricce_package_result[0][0]
        price_package_score = 0
        if price_count > 0:
            price_package_score = 10
        # 获取产品详细报价单
        sql_price_link = "select link from project_price where project_id = %d  and state = 0 ;" % project_id
        sql_price_link_result = Mysql('yellowPageDB').select(sql_price_link)
        if sql_price_link_result is not None:  # 查询结果为空
            price_link = sql_price_link_result[0][0]
            if price_link is not None and price_link != '':
                price_link_score = 5
            else:
                price_link_score = 0
        else:
            price_link_score = 0
            print('该产品不存在定价信息')

        price_score = price_package_score + price_link_score
        print('price_package_score:{},price_link_score:{}'.format(price_package_score, price_link_score))

        return price_score

    def getProjectCommentsScore(self, project_id):
        # 初始化  点评 comment_score
        sql_comments = "select count(1) from project_comments where project_id = %d  and state = 1 ;" % project_id
        sql_comments_result = Mysql('yellowPageDB').select(sql_comments)
        comments_count = sql_comments_result[0][0]
        if 0 <= comments_count <= 10:
            comment_score = comments_count
        elif 11 <= comments_count <= 19:
            comment_score = 10 + 2 * (comments_count - 10)

        elif comments_count >= 20:
            comment_score = 35
        else:
            comment_score = 0
        print('comment_score:', comment_score)
        return comment_score

    # 商家认证得分，不经过归一化处理
    def getBusinessFirm(self, project_id):
        sql_firm = "select count(1) from business_user_project where project_id = %d  and state = 0 ;" % project_id
        sql_firm_result = Mysql('yellowPageDB').select(sql_firm)
        firm_count = sql_firm_result[0][0]
        if firm_count > 0:
            firm_score = 1
        else:
            firm_score = 0
        return firm_score

    # 获取所有产品的分数，并将以上5部分数据合并
    def ProjectCompleteScore(self, project_id=None):
        if project_id is None:
            sql = "select id from project where state= 1 and source = 1;"
            sql_result = Mysql('yellowPageDB').select(sql)
            for i in sql_result:
                project_id = i[0]
                print(project_id)

                base_score = self.getProjectBaseScore(project_id)
                case_score = self.getProjectCaseScore(project_id)
                function_score = self.getProjectFunctionScore(project_id)
                price_score = self.getProjectPriceScore(project_id)
                comment_score = self.getProjectCommentsScore(project_id)
                firm_score = self.getBusinessFirm(project_id)
                score = base_score + case_score + function_score + price_score + comment_score

                # 获取当前时间，插入数据
                created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                sql_insert = "INSERT INTO `project_info_score` ( `project_id`,`base_score`,`case_score`, `function_score`," \
                             "`price_score`,`comment_score`,`firm_score`,`score`, `created_at`)" \
                             " VALUES(%d,%d,%d,%d,%d,%d,%d,%d,'%s');" % (
                                 project_id, base_score, case_score, function_score, price_score, comment_score,
                                 firm_score,
                                 score, created_at)
                # print(sql_insert)
                Mysql('localhost').insert(sql_insert)
        else:
            base_score = self.getProjectBaseScore(project_id)
            case_score = self.getProjectCaseScore(project_id)
            function_score = self.getProjectFunctionScore(project_id)
            price_score = self.getProjectPriceScore(project_id)
            comment_score = self.getProjectCommentsScore(project_id)
            firm_score = self.getBusinessFirm(project_id)
            score = base_score + case_score + function_score + price_score + comment_score
            print(score)

    def MaxAndMin(self):
        sql = "select max(score) ,min(score) from project_info_score;"
        sql_result = Mysql('localhost').select(sql)
        score_max = sql_result[0][0]
        score_min = sql_result[0][1]
        return score_max, score_min

    def NormalProjectInfo(self):
        self.ProjectCompleteScore()
        score_max, score_min = self.MaxAndMin()
        sql = "select id,project_id,score from project_info_score where date(created_at)  = '%s';" % self.current_date
        sql_result = Mysql('localhost').select(sql)
        for i in sql_result:
            if i[2] == 0:
                project_score = 0
            else:
                project_score = Decimal(i[2] - score_min) / (score_max - score_min)
            # 当前时间
            update_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            sql_update = "update project_info_score set normal_score = '%s',updated_at='%s' where id = %d " % (
                project_score, update_at, i[0])
            print(sql_update)
            Mysql('localhost').update(sql_update)


if __name__ == '__main__':
    mm = ProjecctInfoScore()
    mm.ProjectCompleteScore(1097)
