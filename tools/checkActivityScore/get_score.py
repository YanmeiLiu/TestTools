# -*- coding: utf-8 -*-
# @Date : 2021-5-14 11:43
# author:liuyanmei
# 点评得积分活动，查看用户的积分详情
from TestTools.config.db import Mysql


def getActivityTime():
    sql = "select start_time,end_time from track_activity where track_sign='cty2105021' "

    sql_result = Mysql('yellowPageDB').select(sql)
    startTime = sql_result[0][0]
    endTime = sql_result[0][1]
    return startTime, endTime


def getScore(user_id):
    # 获取结束时间，点评的创建时间要小于活动的结束时间
    startTime, endTime = getActivityTime()
    sql = "select user_id,project_id,date(audit_time) from project_comments " \
          "where state = 1 and user_id =%d and  created_at <='%s' and  created_at >='%s' and audit_time<'2021-6-4 23:59:59';" % (
              user_id, endTime, startTime)
    sql_result = Mysql('yellowPageDB').select(sql)
    all_score = 0
    if sql_result:
        for i in sql_result:
            user_id = i[0]
            project_id = i[1]
            audit_date = i[2]
            # 获取产品的名称
            sql_project_name = "select name from project where id =%d and state = 1;" % project_id
            sql_project_name_result = Mysql('yellowPageDB').select(sql_project_name)
            if sql_project_name:
                project_name = sql_project_name_result[0][0]
            # 获取产品是否属于项目管理分类，若是则+500分，不是则是+100分
            sql_kind = "select kind_value from project_kind_related where project_id = %d" % project_id
            sql_kind_result = Mysql('yellowPageDB').select(sql_kind)
            if sql_kind_result:
                for k in sql_kind_result:
                    if k[0] == 1019 or k[0] == 1092:
                        score = 500
                        break
                    else:
                        score = 100
            all_score += score
            print('{}\t 点评{}\t +{}分\t 审核时间:{}\n总分数是:{}'.format(user_id, project_name, score, audit_date, all_score))

        return user_id, all_score


def getAllScore():
    #     根据活动内点评获取所有用户
    startTime, endTime = getActivityTime()
    sql = "select distinct(user_id) from project_comments " \
          "where state = 1 and   created_at <='%s' and  created_at >='%s' and audit_time<'2021-6-4 23:59:59';" % (
              endTime, startTime)
    sql_result = Mysql('yellowPageDB').select(sql)
    # 数组
    score_list = []
    if sql_result:
        for i in sql_result:
            user_list = []
            user_id, all_score = getScore(i[0])
            user_list.append(user_id)
            user_list.append(all_score)
            score_list.append(user_list)
        print(score_list)
        return score_list
    else:
        return ''


# 排名，开发方案：新的数据库表，直接查就行了


if __name__ == '__main__':
    getScore(924)
