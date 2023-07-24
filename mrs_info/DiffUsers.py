import json

from UserInfo import UserInfo, RoleInMrs
from config.db import Mysql


# 根据不同的角色找用户
class DiffUsers(object):
    def __init__(self, user_type, nums, db):
        self.user_type = user_type
        self.nums = nums
        self.db = db
        print("在'{}'环境:".format(self.db))

    def getInfo(self):
        if self.user_type == 0:  # 普通注册用户
            print('普通注册用户')
            sql = "select case when u.user_id is not null and p.id is null and m.id is null and i.id is null then u.user_id end  as user_id " \
                  " from mus.`user_bind_mobile` u " \
                  " left join  pms.pms_company_project_entrepreneur p on u.user_id  = p.user_id and p.status =1" \
                  " left join   pms.pms_investor_manager m  on m.user_id =u.user_id and m.`status`=0" \
                  " left join  pms.pms_investor_ivperson i on i.user_id = u.user_id and i.`status` in (0,1) " \
                  " where u.mobile REGEXP '^2'" \
                  " order by rand() limit %s" % self.nums
            sql_result = Mysql(self.db).select(sql)

        elif self.user_type == 1:  # 创业者
            print('只是创业者：')
            sql = "select case when p.user_id is not null and m.user_id is null then p.user_id end as user_id " \
                  " from  pms_company_project_entrepreneur p left join  pms_investor_manager m  " \
                  " on p.user_id = m.user_id where  p.`status` = 1  order by rand() limit %s;" % self.nums
            sql_result = Mysql(self.db).select(sql)

        elif self.user_type == 2:  # 只是投资管理员
            sql = "select user_id from " \
                  "(select case when m.user_id is not null and p.user_id is null then m.user_id end as user_id " \
                  " from pms_investor_manager m left join  pms_investor_ivperson p   on p.user_id = m.user_id and  " \
                  " p.`status` = 1 ) a where user_id is not null  order by rand() limit %s;" % self.nums
            sql_result = Mysql(self.db).select(sql)
            print('只是投资管理员：')

        elif self.user_type == 3:  # 只是投资人
            sql = "select case when p.user_id is not null and m.user_id is null then p.user_id end as user_id" \
                  " from  pms_investor_ivperson p left join  pms_investor_manager m  on p.user_id = m.user_id" \
                  " and m.status=0 where  p.`status` = 1  order by rand() limit %s;" % self.nums
            sql_result = Mysql(self.db).select(sql)
            print('只是投资人的账号是：')

        elif self.user_type == 4:  # 投资人 & 投资管理员
            print('既是投资管理员又是投资人的账号是：')

            sql = "select  m.user_id from pms_investor_manager m " \
                  " inner join pms_investor_ivperson p on p.user_id = m.user_id and p.`status` = 1" \
                  " where m.`status` =0   order by rand() limit %s;" % self.nums
            sql_result = Mysql(self.db).select(sql)
        elif self.user_type == 5:  # 创业者 & 投资管理员
            print('既是投资管理员又是创业者的账号是：')

            sql = "select  m.user_id from pms_investor_manager m " \
                  " inner join pms_company_project_entrepreneur e on e.user_id = m.user_id  " \
                  " and e.`status` =1 where m.`status` =0  order by rand() limit %s;" % self.nums
            sql_result = Mysql(self.db).select(sql)
        else:
            print('user_type请输入1~5')
            sql_result = False
        print(sql)
        return sql_result


if __name__ == '__main__':
    sql_result = DiffUsers(user_type=1, nums=2, db='pms_test').getInfo()
    # 获取这些账号的手机号
    if sql_result:
        for i in sql_result:
            u = UserInfo(user_id=i[0], db='mus_test')
            user_info, user_id = u.reUserid()
            if user_id:
                user = RoleInMrs(user_id, 'pms_test')
                investor = user.isInvestor()
                user_info.update(investor)
                entrepreneur = user.isEntrepreneur()
                user_info.update(entrepreneur)
                investor_manager = user.isInvestorManager()
                user_info.update(investor_manager)
            print(json.dumps(user_info, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False))
