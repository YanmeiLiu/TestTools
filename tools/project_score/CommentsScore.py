from config.db import Mysql
# 计算单个软件的用户平均分
import time, datetime

from decimal import Decimal
class CommentScore(object):
    # 计算单个软件的用户平均分
    def getSingleComments(self, project_id):
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
                    s = round(score_num / count_comments * score, 16)
                    user_score += s
                else:
                    print('score数据错误')
            print('用户的评分是:{}'.format(user_score))

        else:
            count_comments = sql_result[0][0]
            user_score = 0

        return count_comments, user_score

    def getAllComments(self):
        # 计算都有哪些产品
        # 计算每个产品的分数
        # 插入数据库
        sql = "select id from project where state =1 and source = 1;"
        sql_result = Mysql('yellowPageDB').select(sql)
        for i in sql_result:
            project_id = i[0]
            count_comments, user_score = self.getSingleComments(i[0])
            #         本地数据库插入数据
            # 当前时间
            created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            sql_insert = "INSERT INTO project_user_score " \
                         "(`project_id`, `score_num`, `user_score`, `created_at`)" \
                         " VALUES(%d,%d,%s,'%s');" % (
                             project_id, count_comments, user_score, created_at)
            Mysql('localhost').insert(sql_insert)

    def MaxAndMinUserScore(self):
        sql = "select max(user_score) ,min(user_score) from project_user_score where score_num >0 ;"
        sql_result = Mysql('localhost').select(sql)
        user_score_max = sql_result[0][0]
        user_score_min = sql_result[0][1]
        return user_score_max, user_score_min

    # 用户加权分，归一化处理

    def NormalUserScore(self):
        self.getAllComments()
        user_score_max, user_score_min = self.MaxAndMinUserScore()
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


if __name__ == '__main__':
    mm = CommentScore()
    mm.NormalUserScore()
