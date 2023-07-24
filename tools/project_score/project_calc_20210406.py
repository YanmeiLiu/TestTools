#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 计算企服点评平台产品评分
# user : liuyanmei
# date :2021-1-15
# updated_at :2021-2-8 ，当前已经是第二次改版后的结果

import re
import time
import datetime

from TestTools.config.db import Mysql
from decimal import Decimal


# 查询所有产品中，评论数最多的，评论数最少的
def getMaxAndMinComments():
    sql_max_min = "select max(sum_eva) as max_comments ,min(sum_eva) as min_comments " \
                  "from (select count(*) as sum_eva from project_comments " \
                  "where user_id> 0 and state  =0 " \
                  "and project_id in (select id from project where " \
                  "(created_at >='2020-12-29 00:00:00' and  state = 1) or created_at<'2020-12-29 00:00:00')  " \
                  "group by project_id) as sum_eva;"
    sql_max_min_result = Mysql('yellowPageDB').select(sql_max_min)
    max_comments = sql_max_min_result[0][0]
    min_comments = sql_max_min_result[0][1]
    return max_comments, min_comments


# 所有产品的平均分
# def getAllAvg():
#     #     查询所有的有效评论个数
#     sql = "select count(*)  from project_comments  where  category = 0 and state = 1 and user_id >0 and project_id in (select id from project where state=1);"
#     sql_result = Mysql('yellowPageDB').select(sql)
#     if int(sql_result[0][0]) > 0:  # 有有效评论
#         count_comments = sql_result[0][0]
#         print("目前全部的有效评论个数是：{}".format(count_comments))
#         # 上面评论条数，每一条单独评论的评分计算
#         sql_single_comment = "select id,score,user_id,project_id from project_comments where category = 0  and state = 1 and user_id >0 and project_id in (select id from project where state=1);"
#         sql_single_comment_result = Mysql('yellowPageDB').select(sql_single_comment)
#         total_score = 0
#         for i in range(0, len(sql_single_comment_result)):
#             comment_id = sql_single_comment_result[i][0]
#             score = sql_single_comment_result[i][1] / 5
#             sql_attr = "select project_comments_id,avg(score/10) as attr_avg from project_comments_attr where project_comments_id=%d and value in (10,20,30,40,50,60,70) and score >0;" % comment_id
#             sql_attr_result = Mysql('yellowPageDB').select(sql_attr)
#             # 判断是否存在子评分
#             if sql_attr_result[0][0] == None:  # 不存在
#                 attr_avg = 0
#             else:
#                 attr_avg = sql_attr_result[0][1]
#             single_score = (Decimal(score) / 2 + Decimal(attr_avg)) * 50 / 100
#             # print('user_id = {} 的comment_id = {}的 分数是 {}'.format(sql_single_comment_result[i][2], comment_id,
#             # single_score))
#             print(sql_single_comment_result[i][2], ',', comment_id, ',',
#                   single_score, ',', )
#             # 所有用户的分数之和
#             total_score += single_score
#         avg = round(total_score / count_comments, 18)
#         print('\n所有评论的总分是:{}\n所有评论的平均分是{}'.format(total_score, avg))
#         # 当前时间
#         created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#         sql_insert = "INSERT INTO `project_all_avg`" \
#                      " ( `total_score`, `total_num`, `avg`, `created_at`)" \
#                      " VALUES(%s,'%d',%s,'%s');" % (
#                          total_score, count_comments, avg, created_at)
#         print(sql_insert)
#         Mysql('localhost').insert(sql_insert)
#
#         return avg


# 计算单个软件的用户平均分
def getSingleComments(project_id):
    # 查询某一产品的有效评论个数
    sql = "select count(*)  from project_comments  " \
          "where project_id  = %d and  category = 0 and state = 1 and user_id >0;" % project_id
    sql_result = Mysql('yellowPageDB').select(sql)
    print(sql_result)
    if sql_result[0][0] > 0:  # 有有效评论
        count_comments = sql_result[0][0]
        print('project_id = {}  有效评论个数是:{}'.format(project_id, count_comments))
        # 上面评论条数，每一条单独评论的评分计算
        sql_split_by_score = "select score,count(*) from project_comments where   project_id = %d and  category = 0  and state = 1 and user_id >0 group by score;" % project_id
        sql_split_by_score_result = Mysql('yellowPageDB').select(sql_split_by_score)
        user_score = 0

        for i in sql_split_by_score_result:
            score = i[0] / 5
            score_num = i[1]
            print('score:{},个数：{}'.format(score, score_num))

            if score == 0:
                s = 0
                user_score += s
            elif 1 <= score <= 10:
                s = round(score_num / count_comments * score, 18)
                user_score += s
            else:
                print('score数据错误')
        print('用户的评分是:{}'.format(user_score))

    else:
        count_comments = sql_result[0][0]
        user_score = 0

    return count_comments, user_score


def InsertCommentScore():
    # 计算都有哪些产品
    # 计算每个产品的分数
    # 插入数据库
    sql = "select id from project where state =1;"
    sql_result = Mysql('yellowPageDB').select(sql)
    for i in sql_result:
        project_id = i[0]
        count_comments, user_score = getSingleComments(i[0])
        #         本地数据库插入数据
        # 当前时间
        created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql_insert = "INSERT INTO project_user_score " \
                     "(`project_id`, `score_num`, `user_score`, `created_at`)" \
                     " VALUES(%d,%d,%s,'%s');" % (
                         project_id, count_comments, user_score, created_at)
        Mysql('localhost').insert(sql_insert)


# 产品所在公司的成立年数,行业，是否国际化
def getEnterprise(project_id):
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


# 计算所有软件的用户加权分
def getAllEnterprise():
    sql = "select id from project where state= 1;"
    sql_result = Mysql('yellowPageDB').select(sql)
    for i in sql_result:
        project_id = i[0]
        already_found, industry, industry_num, overseas = getEnterprise(project_id)

        # 本地数据库插入数据
        # 当前时间
        created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql_insert = "INSERT INTO `project_market_span_tmp`" \
                     " ( `project_id`, `industry`, `industry_num`, `has_overseas`, `already_found`, `created_at`)" \
                     " VALUES(%d,'%s',%d,%d,%d,'%s');" % (
                         project_id, industry, industry_num, overseas, already_found, created_at)
        print(sql_insert)
        Mysql('localhost').insert(sql_insert)


# 业务成立时长0.5%


# 归一化计算模块
def Normalization(num, max_num, min_num):
    P = round((num - min_num) / (max_num - min_num), 18)
    return P

# 查看某一企业的信息完善度
def getProjectInfo(project_id):
    """
    基本信息是 project
    公司信息 enterprise
    产品介绍 ent_product
    成功案例 ent_case
    合作品牌 ent_partner
    获奖信息 ent_award
    里程碑  ent_toplist
    :param project_id:
    :return:
    """
    base_info = 0
    enterprise_info = 0
    product_info = 0
    case_info = 0
    partnet_info = 0
    award_info = 0
    toplist_info = 0
    info_count = 0
    sql_project = "select count(*) from project where id = %d ;" % project_id
    sql_project_result = Mysql('yellowPageDB').select(sql_project)
    if sql_project_result[0][0] > 0:
        info_count += 1
        base_info = 1
        print('project表中有数据')
        sql_enterprise = "select count(*) from enterprise where id in (select ent_id from project where id = %d) ;" % project_id
        sql_enterprise_result = Mysql('yellowPageDB').select(sql_enterprise)
        if sql_enterprise_result[0][0] > 0:
            info_count += 1
            enterprise_info = 1
            print('enterprise表中有数据')

        sql_product = "select count(*) from ent_product where project_id = %d;" % project_id
        sql_product_result = Mysql('yellowPageDB').select(sql_product)
        if sql_product_result[0][0] > 0:
            info_count += 1
            product_info = 1
            print('ent_product表中有数据')

        sql_case = "select count(*) from ent_case where project_id = %d;" % project_id
        sql_case_result = Mysql('yellowPageDB').select(sql_case)
        if sql_case_result[0][0] > 0:
            info_count += 1
            case_info = 1
            print('ent_case表中有数据')

        sql_partner = "select count(*) from ent_partner where project_id = %d;" % project_id
        sql_partner_result = Mysql('yellowPageDB').select(sql_partner)
        if sql_partner_result[0][0] > 0:
            info_count += 1
            partnet_info = 1
            print('ent_partner表中有数据')

        sql_award = "select count(*) from ent_award where project_id = %d;" % project_id
        sql_award_result = Mysql('yellowPageDB').select(sql_award)
        if sql_award_result[0][0] > 0:
            info_count += 1
            award_info = 1
            print('ent_award表中有数据')

        sql_toplist = "select count(*) from ent_toplist where project_id = %d;" % project_id
        sql_toplist_result = Mysql('yellowPageDB').select(sql_toplist)
        if sql_toplist_result[0][0] > 0:
            info_count += 1
            toplist_info = 1
            print('ent_toplist表中有数据')
        perfect_level_final_score = round((info_count / 7), 18)
    else:
        base_info = base_info
        enterprise_info = enterprise_info
        product_info = product_info
        case_info = case_info
        partnet_info = partnet_info
        award_info = award_info
        toplist_info = toplist_info
        info_count = info_count
        print('该project_id = {}不存在'.format(project_id))
        perfect_level_final_score = 0
    print('该project_id = {} 完善信息率是：{}'.format(project_id, perfect_level_final_score))

    return project_id, info_count, base_info, enterprise_info, product_info, case_info, partnet_info, award_info, toplist_info, perfect_level_final_score

# 计算所有企业的信息完善度
def getAllInfo():
    sql = "select id from project where state =1 ;"
    sql_result = Mysql('yellowPageDB').select(sql)
    for i in sql_result:
        project_id = i[0]
        print(project_id)
        project_id, \
        info_count, \
        base_info, \
        enterprise_info, \
        product_info, \
        case_info, \
        partnet_info, \
        award_info, \
        toplist_info, \
        perfect_level_final_score = getProjectInfo(project_id)

        # 本地数据库插入数据
        # 当前时间
        created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql_insert = "INSERT INTO `product_info_quality_final`" \
                     " ( `project_id`,`total_num`, `base_info`, `enterprise_info`, `product_info`, `case_info`, " \
                     "`partnet_info`,`award_info`, `toplist_info`, `perfect_level_final_score`, `business_firm_final_score`," \
                     " `operate_intervene_final_score`, `created_at`)" \
                     " VALUES(%d,%d,%d,%d,%d,%d,%d,%d,%d,%s,%d,%d,'%s');" % (project_id, info_count, base_info,
                                                                             enterprise_info,
                                                                             product_info,
                                                                             case_info,
                                                                             partnet_info,
                                                                             award_info,
                                                                             toplist_info,
                                                                             perfect_level_final_score, 0, 0, created_at
                                                                             )
        print(sql_insert)
        Mysql('localhost').insert(sql_insert)


# 判断是否上市企业，融资金额
def ifInternatioal(project_id):
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
            elif i[1] in ['种子轮', '天使轮', 'Pre-A轮', 'A轮', 'A+轮', 'B轮', 'B+轮', 'C轮', 'C+轮', 'D轮', 'D+轮', 'E轮', 'E+轮', 'F轮',
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
def calRound():
    sql = "select id from project where state =1;"
    sql_result = Mysql('yellowPageDB').select(sql)
    for i in sql_result:
        project_id = i[0]
        print(project_id)
        s, financing_count, total_amount = ifInternatioal(project_id)

        # 当前时间
        created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql_insert = "INSERT INTO `project_round` ( `project_id`, `amount`, `round`, `ipo`, `created_at`)" \
                     " VALUES(%d,%d,%d,%d,'%s');" % (
                         project_id, total_amount, financing_count, s, created_at)
        Mysql('localhost').insert(sql_insert)


# 有关联的文章数
def getArticle(project_id):
    sql = "select count(distinct(product_evaluation_id)) from product_evaluation_related " \
          "where project_id = %d " \
          "and product_evaluation_id in (select id from product_evaluation where  state=1);" % project_id
    sql_result = Mysql('yellowPageDB').select(sql)
    article_num = sql_result[0][0]
    print('project_id = {}关联了{}篇文章'.format(project_id, article_num))
    return project_id, article_num


def getAllArticle():
    sql = "select id from project where state =1;"
    sql_result = Mysql('yellowPageDB').select(sql)
    for i in sql_result:
        project_id = i[0]
        project_id, article_num = getArticle(project_id)
        # 当前时间
        created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql_insert = "INSERT INTO `project_article` ( `project_id`, `article_num`,  `created_at`)" \
                     " VALUES(%d,%d,'%s');" % (
                         project_id, article_num, created_at)
        print(sql_insert)
        Mysql('localhost').insert(sql_insert)


# 获取当前product_id的最近7天的平均值
def getIndexSpider(project_id, project_name, project_website, start_date, end_date):
    sql = "select  product_id,product_name,website,baidu_search_num,weixin_articles_num,zhihu_articles_num,baidu_include_num " \
          "from index_spider where product_id =%d and spider_date >='%s'  and spider_date<'%s' order by id desc ;" % (
              project_id, start_date, end_date)
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


def getAllIndexSpider():
    # 获取当前日期
    current_day = datetime.datetime.now()
    days = datetime.timedelta(days=7)
    start_date = current_day - days
    start_date_to = datetime.datetime(start_date.year, start_date.month, start_date.day)
    end_date_to = datetime.datetime(current_day.year, current_day.month, current_day.day)

    end_date = str(end_date_to)[0:10]
    start_date = str(start_date_to)[0:10]
    print('从{}开始获取'.format(start_date))
    sql = "select id,name,website from project where state =1 ;"
    sql_result = Mysql('yellowPageDB').select(sql)
    for i in sql_result:
        baidu, baidu_num, baidu_avg, \
        baidu_include, baidu_include_num, baidu_include_avg, \
        weixin, weixin_num, weixin_avg, \
        zhihu, zhihu_num, zhihu_avg = getIndexSpider(i[0], i[1], i[2], start_date, end_date)
        # 当前时间
        created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql_insert = "INSERT INTO `index_7days_avg` ( `project_id`,`baidu_total`,`baidu_num`, `baidu_avg`," \
                     "`weixin_total`,`weixin_num`,`weixin_avg`," \
                     "`zhihu_total`,`zhihu_num`,`zhihu_avg`, " \
                     "`baidu_include_total`,`baidu_include_num`,`baidu_include_avg`, " \
                     " `created_at`)" \
                     " VALUES(%d,%d,%d,%s,%d,%d,%s,%d,%d,%s,%d,%d,%s,'%s');" % (
                         i[0], baidu, baidu_num, baidu_avg, weixin, weixin_num, weixin_avg, zhihu, zhihu_num, zhihu_avg,
                         baidu_include, baidu_include_num, baidu_include_avg,
                         created_at)
        print(sql_insert)
        Mysql('localhost').insert(sql_insert)


def MaxAndMinUserScore():
    sql = "select max(user_score) ,min(user_score) from project_user_score where score_num >0 ;"
    sql_result = Mysql('localhost').select(sql)
    user_score_max = sql_result[0][0]
    user_score_min = sql_result[0][1]
    return user_score_max, user_score_min


def MaxAndMinSpider():
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


def MaxAndMinRound():
    sql = "select max(round) ,min(round) from project_round  ;"
    sql_result = Mysql('localhost').select(sql)
    round_max = sql_result[0][0]
    round_min = sql_result[0][1]
    return round_max, round_min


def MaxAndMinAmount():
    sql = "select max(amount) ,min(amount) from project_round  ;"
    sql_result = Mysql('localhost').select(sql)
    amount_max = sql_result[0][0]
    amount_min = sql_result[0][1]
    return amount_max, amount_min


def MaxAndMinFound():
    sql = "select max(already_found) ,min(already_found) from project_market_span_tmp where already_found>=0 ;"
    sql_result = Mysql('localhost').select(sql)
    found_max = sql_result[0][0]
    found_min = sql_result[0][1]
    return found_max, found_min


def MaxAndMinArticle():
    sql = "select max(article_num) ,min(article_num) from project_article ;"
    sql_result = Mysql('localhost').select(sql)
    article_max = sql_result[0][0]
    article_min = sql_result[0][1]
    return article_max, article_min


def MaxAndMinIndustry():
    sql = "select max(industry_num) ,min(industry_num) from project_market_span_tmp where industry_num>=0 ;"
    sql_result = Mysql('localhost').select(sql)
    industry_max = sql_result[0][0]
    industry_min = sql_result[0][1]
    return industry_max, industry_min


# 用户加权分，归一化处理

def NormalUserScore():
    user_score_max, user_score_min = MaxAndMinUserScore()
    sql = "select project_id,user_score from project_user_score  ;"
    sql_result = Mysql('localhost').select(sql)
    for i in sql_result:
        if i[1] == 0:
            final_user_score = 0
        else:

            final_user_score = Decimal(i[1] - user_score_min) / (user_score_max - user_score_min)
        # 当前时间
        created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql_insert = "INSERT INTO `project_user_score_final` " \
                     "( `project_id`,`user_score_max`, `user_score_min`,  `user_score`,`final_user_score`, `created_at`)" \
                     " VALUES(%d,%s,%s,%s,%s,'%s'); " % (
                         i[0], user_score_max, user_score_min, i[1], final_user_score, created_at)
        print(sql_insert)
        Mysql('localhost').insert(sql_insert)


def NormalSpider():
    baidu_avg_max, baidu_avg_min, weixin_avg_max, weixin_avg_min, zhihu_avg_max, zhihu_avg_min, baidu_include_avg_max, baidu_include_avg_min = MaxAndMinSpider()

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


def NormalRoundAndAmount():
    round_max, round_min = MaxAndMinRound()
    amount_max, amount_min = MaxAndMinAmount()
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
                             i[0], i[1], round_max, round_min, round_score, i[2], amount_max, amount_min, amount_score,
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


def NormalArticle():
    article_max, article_min = MaxAndMinArticle()
    sql = "select project_id,article_num from project_article  ;"
    sql_result = Mysql('localhost').select(sql)
    for i in sql_result:
        if i[1] == 0:
            article_score = 0
        else:

            article_score = Decimal(i[1] - article_min) / (article_max - article_min)
        # 当前时间
        created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql_insert = "INSERT INTO `project_articel_score`" \
                     " (`project_id`, `article_num`, `article_score`, `article_max`, `article_min`, `created_at`) " \
                     "VALUES (%d,%d,%s,%d,%d,'%s'); " % (
                         i[0], i[1], article_score, article_max, article_min, created_at)
        print(sql_insert)
        Mysql('localhost').insert(sql_insert)


def NormalFoundAndIndustry():
    industry_max, industry_min = MaxAndMinIndustry()
    found_max, found_min = MaxAndMinFound()
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


# 计算最后
def calLast(project_id):
    # 计算最后的用户评分40%
    sql = "select final_user_score from project_user_score_final where project_id = %d;" % project_id
    sql_result = Mysql('localhost').select(sql)
    if sql_result:
        final_user_score = float(sql_result[0][0])
        user_score = final_user_score * 40 / 100
    else:
        user_score = 0
    # 计算最后的企业信息质量5%，信息完善度 2.5%
    sql_info = "select perfect_level_final_score,business_firm_final_score,operate_intervene_final_score " \
               "from product_info_quality_final where project_id = %d;" % project_id
    sql_info_result = Mysql('localhost').select(sql_info)
    if sql_info_result:
        perfect_level_final_score = float(sql_info_result[0][0])
        business_firm_final_score = float(sql_info_result[0][1])
        operate_intervene_final_score = float(sql_info_result[0][2])
        info_score = perfect_level_final_score * 2.5 / 100 + (
                business_firm_final_score + operate_intervene_final_score) * 1.25 / 100
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
    print('project_id = {} 的user_score{},\nbrand_score:{},\ninfo_score:{}'.format(project_id, user_score, brand_score,
                                                                                  info_score))
    return user_score, brand_score, info_score


def getAllScore():
    sql = "select id from project where state =1;"
    sql_result = Mysql('yellowPageDB').select(sql)
    for i in sql_result:
        user_score, brand_score, info_score = calLast(int(i[0]))
        total_score = user_score + brand_score + info_score
        # 当前时间
        created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql_insert = "INSERT INTO `user_brand_info_score` ( `project_id`, `user_score`, `brand_heat_score`, `info_score`, `total_score`,`created_at`)" \
                     "VALUES(%d,%s,%s,%s,%s,'%s'); " % (
                         i[0], user_score, brand_score, info_score, total_score, created_at)
        print(sql_insert)
        Mysql('localhost').insert(sql_insert)




if __name__ == '__main__':
    # 获取所有企业的信息
    # getAllInfo()
    # # 获取所以关联文章的信息
    # getAllArticle()
    # # 获取所有的industry found
    # getAllEnterprise()
    # # 计算所有企业的融资数额
    # calRound()
    # # 外部平台指数
    # getAllIndexSpider()
    # # 归一化外部平台指数
    NormalSpider()
    # # 归一化关联文章数
    NormalArticle()
    # # 归一化融资轮次，金额
    NormalRoundAndAmount()
    # # 归一化创建时间，行业
    NormalFoundAndIndustry()
    # #计算每个产品的评论分数
    InsertCommentScore()
    # # # 归一化计算用户评分
    NormalUserScore()
    #
    # # chan()
    # # 计算单个软件的最后得分
    calLast(2660)
    # # 计算所有软件的最后得分
    getAllScore()
    # getSort(2297)
    # getSingleComments(1089)
