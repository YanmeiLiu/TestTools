# -*- coding: utf-8 -*-
# @Date : 2021-4-19 15:34
# author:liuyanmei
# 从用户点评中判断客户规模&评价

"""
输入一个产品id，获取到该产品的所有有效评论
根据 group_num判断规模
不同的规模之和占比
"""
from decimal import Decimal

from TestTools.config.db import Mysql


# 根据名字获取到id
def get_id(name):
    sql = "select id from project where name ='%s' and state =1;" % name
    sql_result = Mysql('yellowPageDB').select(sql)
    if sql_result:
        project_id = sql_result[0][0]
        return project_id
    else:
        return 0


class Project_Rate(object):
    def __init__(self, project_id):
        self.project_id = project_id

    def get_project_info(self):
        sql = "select p.id,p.name,e.full_name,date(e.founded_at) as founded ,e.latest_financing from project p  join enterprise e on p.ent_id = e.id" \
              " where p.id=%d;" % self.project_id
        sql_result = Mysql('yellowPageDB').select(sql)
        print(sql)
        if sql:
            project_id = sql_result[0][0]
            project_name = sql_result[0][1]
            ent_name = sql_result[0][2]
            founded_at = sql_result[0][3]
            latest_financing = sql_result[0][4]
            print('project_id:{}的名称是:{}\n'
                  '所属公司:{}\n'
                  '成立年份：{}\n'
                  '融资信息：{}'.format(self.project_id, project_name, ent_name, founded_at, latest_financing))
        #     获取分类信息
        sql_kind = "select r.project_id,p.name,r.is_main,k.text from project_kind_related r " \
                   "join project p on r.project_id = p.id " \
                   "join project_kind k on r.kind_value = k.value where p.id =%d and k.state =0 order by r.id asc;" % self.project_id
        sql_kind_result = Mysql('yellowPageDB').select(sql_kind)
        if sql_kind_result:
            for i in sql_kind_result:
                p_name = i[1]
                is_main = i[2]
                kind_text = i[3]
                print('所属分类是:{}，是否主分类:{}'.format(kind_text, is_main))
        #     获取定价信息
        sql_price = "select is_free from project_price where state = 0 and project_id =%s;" % self.project_id
        sql_price_result = Mysql('yellowPageDB').select(sql_price)
        print(sql_price)
        if sql_price_result:
            is_free = sql_price_result[0][0]
            if is_free == 0:
                print('是否支持免费：否')
            else:
                print('是否支持免费：是')
        else:
            print('是否支持免费： ')
        sql_price_detail = "select name,price,price_description, combo_description from project_price_detail " \
                           "where state = 0 and project_id = %d order by sort desc,id asc;" % self.project_id
        sql_price_detail_result = Mysql('yellowPageDB').select(sql_price_detail)
        if sql_price_detail_result:
            for i in sql_price_detail_result:
                name, price, price_description, combo_description = i
                print('套餐名：{}\n'
                      '价格：{}\n'
                      '定价描述:{}\n'
                      '套餐描述:{}'.format(name, price, price_description, combo_description))
        else:
            print('无套餐信息')

    # 对比页面的客户规模占比
    def GroupNumRate(self):
        sql = "select project_id,score,group_num from project_comments where state =1 and project_id =%d and group_num >0;" % self.project_id
        sql_result = Mysql('yellowPageDB').select(sql)
        small_num = mid_num = big_num = 0
        small_score = mid_score = big_score = 0

        if sql_result:
            for i in sql_result:
                group_num = i[2]
                if 1 <= group_num <= 3:
                    small_score += i[1]
                    small_num += 1
                elif 4 <= group_num <= 6:

                    mid_score += i[1]
                    mid_num += 1
                elif 7 <= group_num <= 9:
                    big_score += i[1]
                    big_num += 1
                # else:
                #     print('group_num={}不计入统计'.format(group_num))

        if small_num > 0:
            small_last = Decimal(small_score / small_num)
            small_rate = Decimal(small_num / len(sql_result))
        else:
            small_last = 0
            small_rate = 0
        if mid_num > 0:
            mid_last = Decimal(mid_score / mid_num)
            mid_rate = Decimal(mid_num / len(sql_result))

        else:
            mid_last = 0
            mid_rate = 0
        if big_num > 0:
            big_last = Decimal(big_score / big_num)
            big_rate = Decimal(big_num / len(sql_result))

        else:
            big_last = 0
            big_rate = 0

        print('小型企业：{}，评论条数：{}\n'
              '中型企业：{}，评论条数：{}\n'
              '大型企业：{}，评论条数：{}\n'.format(round(small_last / 10, 1), small_num, round(mid_last / 10, 1), mid_num,
                                         round(big_last / 10, 1), big_num))

        return small_last, mid_last, big_last

    # 对比b报告的客户规模占比
    def CustomerRate(self):
        # 第一步计算评论者的企业占比
        sql = "select project_id,score,group_num from project_comments where state =1 and project_id =%d and group_num >0;" % self.project_id
        sql_result = Mysql('yellowPageDB').select(sql)
        small_num = mid_num = big_num = 0

        if sql_result:
            for i in sql_result:
                group_num = i[2]
                if 1 <= group_num <= 3:
                    small_num += 1
                elif 4 <= group_num <= 6:

                    mid_num += 1
                elif 7 <= group_num <= 9:
                    big_num += 1

        # 第二步，计算成功案例的企业规模占比
        sql_case = "select scale from brand where id in (select brand_id from ent_case where state =0 and project_id =%d);" % self.project_id
        sql_case_result = Mysql('yellowPageDB').select(sql_case)
        case_small_num = case_mid_num = case_big_num = 0

        if sql_case_result:
            for i in sql_case_result:
                scale = i[0]
                if 10 <= scale <= 20:
                    case_small_num += 1
                elif 30 <= scale <= 50:

                    case_mid_num += 1
                elif scale > 50:
                    case_big_num += 1

        # 第三步，计算合作品牌的企业规模占比
        sql_partner = "select scale from brand where id in (select brand_id from ent_partner where state =0 and project_id =%d);" % self.project_id
        sql_partner_result = Mysql('yellowPageDB').select(sql_partner)
        partner_small_num = partner_mid_num = partner_big_num = 0

        if sql_partner_result:
            for i in sql_partner_result:
                scale = i[0]
                if 10 <= scale <= 20:
                    partner_small_num += 1
                elif 30 <= scale <= 50:

                    partner_mid_num += 1
                elif scale > 50:
                    partner_big_num += 1

        small_all = small_num + case_small_num + partner_small_num
        mid_all = mid_num + case_mid_num + partner_mid_num
        big_all = big_num + case_big_num + partner_big_num
        all = small_all + mid_all + big_all

        if small_all > 0:
            small_rate = Decimal(small_all / all)
        else:
            small_rate = 0
        if mid_all > 0:
            mid_rate = Decimal(mid_all / all)
        else:
            mid_rate = 0
        if big_all > 0:
            big_rate = Decimal(big_all / all)
        else:
            big_rate = 0

        print('总数据是：{},小型企业：{}%,{}\n'
              '中型企业：{}%,{}\n'
              '大型企业：{}%,{}\n'.format(all, round((small_rate) * 100, 1), small_all,
                                     round((mid_rate) * 100, 1), mid_all,
                                     round((big_rate) * 100, 1), big_all))

    # 计算评价详情
    def CommetAttrRate(self):
        sql = "select project_id,id,score from project_comments where state =1 and project_id =%d;" % self.project_id
        sql_result = Mysql('yellowPageDB').select(sql)
        low_score_num = 0
        high_score_num = 0
        easy = service = need = cost = 0
        easy_num = service_num = need_num = cost_num = 0

        if sql_result:
            for i in sql_result:
                # 先获取计算推荐值的数据
                score = i[2]
                # print(score/5)
                if 0 <= score / 5 <= 6:
                    low_score_num += 1
                elif 9 <= score / 5 <= 10:
                    high_score_num += 1
                # else:
                #     print('不计入！')

                # 获取计算每个属性的值的数据

                sql_attr = "select `project_comments_id`,`value`,`score` from project_comments_attr where state =0 and project_comments_id =%d and score>0;" % \
                           i[1]
                sql_attr_result = Mysql('yellowPageDB').select(sql_attr)
                for j in sql_attr_result:
                    value = j[1]
                    if value == 50:
                        easy += j[2]
                        easy_num += 1
                        # print(easy_num,easy)

                    elif value == 60:
                        service += j[2]
                        service_num += 1
                    elif value == 40:
                        need += j[2]
                        need_num += 1
                    elif value == 70:
                        cost += j[2]
                        cost_num += 1
                    # 计算净推荐值

            print(high_score_num, low_score_num)
            recommend = high_score_num / len(sql_result) - low_score_num / len(sql_result)
            if recommend > 0:
                recommend_last = recommend
            else:
                recommend_last = 0
        else:
            recommend_last = 0
            easy = service = need = cost = 0
            easy_num = service_num = need_num = cost_num = 0

        # 计算子项值
        if easy_num != 0:
            easy_score = Decimal(easy / 10 / easy_num)
        else:
            easy_score = 0
        if service_num != 0:
            service_score = Decimal(service / 10 / service_num)
        else:
            service_score = 0
        if need_num != 0:
            need_score = Decimal(need / 10 / need_num)
        else:
            need_score = 0
        if cost_num != 0:
            cost_score = Decimal(cost / 10 / cost_num)
        else:
            cost_score = 0
        print(need_score, easy_score, cost_score, service_score)

        print('净推荐值：{}%\n'
              '需求满足度：{}，评论条数：{}\n'
              '易用性：{}，评论条数：{}\n'
              '性价比：{}，评论条数：{}\n'
              '售后服务：{}，评论条数：{}\n'.format(round(recommend_last, 3) * 100, round(need_score, 1), need_num,
                                         round(easy_score, 1), easy_num,
                                         round(cost_score, 1),
                                         cost_num,
                                         round(service_score, 1), service_num))

        return recommend_last, easy_score, service_score, need_score, cost_score


# 获取产品的主分类分类
# class CompareHistory(object):
#     def __init__(self,pids):
#         self.pids = pids
#     def decode_pids(self):


def getKind_1(project_id, is_main=1):
    sql = "select r.id,r.project_id,r.kind_value,r.is_main,r.state,k.text " \
          "from project_kind_related r   join project_kind  k on r.kind_value = k.value " \
          "where r.project_id =%d and k.state = 0 and r.is_main =%d ;" % (project_id, is_main)
    sql_result = Mysql('yellowPageDB').select(sql)
    if sql_result:
        return sql_result[0][5]
    else:

        return False


def getKind_0(project_id, is_main=0):
    sql = "select r.id,r.project_id,r.kind_value,r.is_main,r.state,k.text " \
          "from project_kind_related r   join project_kind  k on r.kind_value = k.value " \
          "where r.project_id =%d and k.state = 0  and r.is_main =%d  order by id asc limit 1;" % (project_id, is_main)
    sql_result = Mysql('yellowPageDB').select(sql)
    if sql_result:
        # print(sql)
        return sql_result[0][5]
    else:
        return False


def getLastKind(project_id_1, project_id_2, project_id_3=None, project_id_4=None):
    kind_1 = getKind_1(project_id_1)
    if kind_1:
        print(kind_1)
        return kind_1
    else:
        kind_2 = getKind_1(project_id_2)
        if kind_2:
            return kind_2
        else:
            if project_id_3 == None:
                kind_11 = getKind_0(project_id_1)
                if kind_11:
                    return kind_11
                else:
                    kind_22 = getKind_0(project_id_2)
                    if kind_22:
                        return kind_22
                    else:
                        return False
            else:

                kind_3 = getKind_1(project_id_3, is_main=1)
                if kind_3:
                    return kind_3
                else:
                    if project_id_4 == None:
                        kind_11 = getKind_0(project_id_1)
                        if kind_11:
                            return kind_11
                        else:
                            kind_22 = getKind_0(project_id_2)
                            if kind_22:
                                return kind_22
                            else:
                                kind_33 = getKind_0(project_id_3)
                                if kind_33:
                                    return kind_33
                                else:
                                    return False
                    else:
                        print('111', project_id_4)
                        kind_4 = getKind_1(project_id_4, is_main=1)
                        if kind_4:
                            return kind_4
                        else:
                            kind_11 = getKind_0(project_id_1)
                            if kind_11:
                                return kind_11
                            else:
                                kind_22 = getKind_0(project_id_2)
                                if kind_22:
                                    return kind_22
                                else:
                                    kind_33 = getKind_0(project_id_3)
                                    if kind_33:
                                        return kind_33
                                    else:
                                        kind_44 = getKind_0(project_id_4)
                                        if kind_44:
                                            return kind_44
                                        else:
                                            return False


if __name__ == '__main__':
    # 面包屑的分类
    get_id_1 = get_id('云眼AB测试')
    get_id_2 = get_id('简道云')
    get_id_3 = get_id('闪电报销')
    get_id_4 = get_id('Teambition')
    kind_text = getLastKind(get_id_1, get_id_2)
    print('类目应该是：', kind_text)
    print('#' * 50)

    # 单个产品的信息
    PR_1 = Project_Rate(get_id_1)
    PR_1.get_project_info()
    PR_1.CommetAttrRate()
    PR_1.CustomerRate()

    print('#' * 50)
    PR_2 = Project_Rate(get_id_2)
    PR_2.get_project_info()
    PR_2.CommetAttrRate()
    PR_2.CustomerRate()

    print('#' * 50)
    PR_3 = Project_Rate(get_id_3)
    PR_3.get_project_info()
    PR_3.CommetAttrRate()
    PR_3.CustomerRate()

    print('#' * 50)

    PR_4 = Project_Rate(get_id_4)
    PR_4.get_project_info()
    PR_4.CommetAttrRate()
    PR_4.CustomerRate()
