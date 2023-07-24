from config.db import Mysql


def getDiffInvestor(condation):
    sql = "select * from (select a.id,a.investor_name,a.status,a.`管理员`,a.`关联的投资人`,a.`认证通过的投资人`," \
          "a.`待审核的投资人`,ifnull(b.`投资数`,0) `投资数` " \
          "from (select  i.id,i.investor_name,i.`status`," \
          "count(distinct case when m.id is not null and m.status =0  then m.id end ) `管理员`," \
          "count(distinct case when p.id is not null and p.status in (0,1) then p.id end ) `关联的投资人`," \
          "count(distinct case when p.id is not null and p.`status` =1 then p.id end ) `认证通过的投资人`," \
          "count(distinct case when p.id is not null and p.`status` =0 then p.id end ) `待审核的投资人`" \
          " from pms_investor i left join pms_investor_manager m on i.id = m.investor_id " \
          "left join pms_investor_ivperson p on p.investor_id=i.id group by i.id,i.investor_name" \
          ") a left join" \
          "(SELECT investor_source_id,count(1) `投资数` from  pms_company_financing_investor GROUP BY investor_source_id) b" \
          " on a.id  = b.investor_source_id ) t "
    sql = sql + condation
    print(sql)
    sql_result = Mysql('pms_test').select(sql)
    # print(sql)
    if sql_result:
        print(sql_result)
        return sql_result
    else:
        print('没符合条件的数据')
        return


# 查询机构关联的数据
class InvestorInfo(object):
    def __init__(self, investor_id, db):
        self.investor_id = investor_id
        self.db = db

    def getInvestor(self):
        sql = "select id,investor_name,status,deleted " \
              "from pms_investor where id=%s ;" % self.investor_id
        sql_result = Mysql(self.db).select(sql)
        # print(sql_result)
        if sql_result:
            if sql_result[0][3] == 0:
                if sql_result[0][2] == 0:
                    print("机构id：{}\t 机构名称：{}\t 机构状态：草稿".format(sql_result[0][0], sql_result[0][1]))
                elif sql_result[0][2] == 1:
                    print("机构id：{}\t 机构名称：{}\t 机构状态：已上线".format(sql_result[0][0], sql_result[0][1]))
                elif sql_result[0][2] == -1:
                    print("机构id：{}\t 机构名称：{}\t 机构状态：已下线".format(sql_result[0][0], sql_result[0][1]))
                else:
                    print("机构id：{}\t 机构名称：{}\t 机构状态：状态错误".format(sql_result[0][0], sql_result[0][1]))
            else:
                print("机构id：{}\t 机构名称：{}\t 机构状态：已删除".format(sql_result[0][0], sql_result[0][1]))

            return sql_result
        else:
            print("机构不存在")
            return

    # 根据机构id查询是否有管理员
    def hasManager(self):
        sql = "select user_id,investor_id,real_name from pms_investor_manager where `status` = 0 and investor_id = %s;" % self.investor_id
        sql_result = Mysql(self.db).select(sql)
        if sql_result:  # 一个投资人只有一条数据
            print('管理员:yes')
            return True
        else:
            print('管理员:no')

    # 判断是否有投资人
    def hasInvestor(self):
        sql = "SELECT  count(case when `status` = 1 then 1 end )`已认证投资人`," \
              "count(case when `status`= 0 then 1 end )`待审核投资人` " \
              "from pms_investor_ivperson where investor_id = %s ;" % self.investor_id
        sql_result = Mysql(self.db).select(sql)
        print(sql)
        if int(sql_result[0][0]) + int(sql_result[0][1]) > 0:
            print("有{}个投资人，其中{}个已认证{}个待审核".format(sql_result[0][0] + sql_result[0][1], sql_result[0][0],
                                                                 sql_result[0][1]))
        else:
            print("没有关联的投资人（包括待审核和已通过）")

    # 判断在是否有基金管理人
    def hasFundManager(self):
        sql = "select count(1)  from pms_investor_fund_manager where deleted = 0 and investor_id  = %s  ;" % (
            self.investor_id)
        sql_result = Mysql(self.db).select(sql)
        # print(sql)
        if int(sql_result[0][0]) > 0:
            print("基金管理人:has")
        else:
            print("基金管理人:no")

    def hasFinancing(self):
        sql = "select count(DISTINCT f.id) `投资事件`," \
              "count(distinct case when f.investor_hide=0  then f.id end ) `未隐藏投资` ," \
              "count(distinct case when f.investor_hide=1  then f.id end ) `隐藏投资`" \
              " from pms_company_financing_investor fi" \
              " inner join pms_company_financing f on f.id = fi.financing_id " \
              "inner join pms_company_project p on p.company_id=f.company_id and p.project_status = 9  " \
              "where fi.investor_source_id=%s;" % self.investor_id
        sql_result = Mysql(self.db).select(sql)
        if int(sql_result[0][1]) > 0:
            print("投资事件>0")
        else:
            print("没有投资事件")


if __name__ == '__main__':
    # # 这个是只有管理员
    # investro_id = getDiffInvestor(condation="where `管理员` =0 and `关联的投资人` =0  and `status`=1 and  `投资数`=0  limit 10 ")
    # # 这个是只有管理员且有投资数的
    # investro_id = getDiffInvestor(
    # condation="where `管理员` >0 and `关联的投资人` =0  and `status`=1 and `投资数`>0 limit 10 ")

    i = InvestorInfo(2332641742288385, 'pms_test')
    aa = i.getInvestor()
    if aa:
        i.hasInvestor()
        i.hasManager()
        i.hasFundManager()
        i.hasFinancing()