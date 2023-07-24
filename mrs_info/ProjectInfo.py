import json

from config.db import Mysql
from config.setconfig import get_dir
from tools.opt_file.optFiles import ReadFileAsDF, writeToExcelFile


# 查询 项目
class ProjectInfo(object):
    def __init__(self, project_id=None, name=None, db='pms_test'):
        self.project_id = project_id
        self.name = name
        self.db = db
        # self.project_pd = pd.DataFrame()

    def getProjectByName(self):
        sql = "select id " \
              "from project where name='%s' ;" % self.name
        sql_result = Mysql(self.db).select(sql)
        print(sql)
        if sql_result:
            return sql_result
        else:
            return

    def getProject(self):
        if self.name is None and self.project_id is None:
            print('至少输入一个查询条件，项目名称 或  项目id')
            project = {'code': 999, 'msg': '至少输入一个查询条件，项目名称 或  项目id'}
        elif self.project_id is not None:
            self.project_id = self.project_id
        else:  # 根据名字查询
            project_id = self.getProjectByName()
            if project_id:
                self.project_id = project_id[0][0]
            else:
                print('该项目不存在')
                project = {'code': 1, 'msg': '项目不存在'}
        if self.project_id:
            sql = "select id,name,project_status " \
                  "from pms_company_project where id=%s ;" % self.project_id
            sql_result = Mysql(self.db).select(sql)
            # print(sql_result)
            if sql_result:  # 项目已入库
                if sql_result[0][2] == 9:
                    print("project_id：{}\t 项目名称：{}\t 项目状态：已发布".format(sql_result[0][0], sql_result[0][1]))
                    project = {"code": 0, "project_id": sql_result[0][0], "project_name": sql_result[0][1],
                               "project_status": "已发布"}

                elif sql_result[0][2] == 1:
                    print("project_id：{}\t 项目名称：{}\t 项目状态：已下线".format(sql_result[0][0], sql_result[0][1]))
                    project = {"code": 0, "project_id": sql_result[0][0], "project_name": sql_result[0][1],
                               "project_status": "已下线"}
                else:
                    print("project_id：{}\t 项目名称：{}\t 项目状态：状态错误".format(sql_result[0][0], sql_result[0][1]))
                    project = {"code": 0, "project_id": sql_result[0][0], "project_name": sql_result[0][1],
                               "project_status": "状态错误"}
            else:
                # 项目尚未入库，从待审核的里边找
                sql = "SELECT target_id,name  from draft_company_project where target_id = %s" % self.project_id
                sql_result = Mysql(self.db).select(sql)
                if sql_result:
                    print("项目id：{}\t 项目名称：{}\t 项目状态：入驻待审核".format(sql_result[0][0], sql_result[0][1]))
                    project = {"code": 0, "project_id": sql_result[0][0], "project_name": sql_result[0][1],
                               "project_status": "入驻待审核"}

                else:
                    print("项目不存在")
                    project = {"code": 1, "msg": "项目不存在"}
        return project

    # 根据项目id查询是否有认领人
    def hasEntrepreneur(self):
        sql = "select project_id,count(1) `认领人数` from pms_company_project_entrepreneur where `status` = 1 and " \
              "project_id = %s;" % self.project_id
        sql_result = Mysql(self.db).select(sql)
        # print(sql)
        if sql_result:  # 有认领人
            print('认领人：{}个'.format(sql_result[0][1]))
            entp = {"entrepreneur_num": sql_result[0][1]}
        else:  # 没有认领人
            print('认领人:×')
            entp = {"entrepreneur_num": 0}
        return entp

    # 判断是否有待审核的认领人
    def hasDraftEntrepreneur(self):
        # 入驻项目时的认领人
        sql = "select count(distinct de.id) from draft_company_project_entrepreneur  de " \
              "inner join draft_company_project dp on dp.name =de.project_name and dp.target_id=  %s where de.status " \
              "=0 ;" % self.project_id
        sql_result = Mysql(self.db).select(sql)
        # print(sql)
        if sql_result[0][0] > 0:
            print("有{}个待审核的入驻认领人".format(sql_result[0][0]))
            draft_entp = {"draft_entrepreneur_num": sql_result[0][0]}
        else:
            # 认领审核的待认证人
            sql = "select count(1) from pms_authentication_entrepreneur where status = 0 and project_id=%s " % self.project_id
            sql_result = Mysql(self.db).select(sql)
            if sql_result[0][0] > 0:
                print("有{}个待审核的认领人".format(sql_result[0][0]))
                draft_entp = {"draft_entrepreneur_num": sql_result[0][0]}

            else:
                print("待审核的认领人：×")
                draft_entp = {"draft_entrepreneur_num": 0}
        return draft_entp

    # 判断在是否有待审核记录
    def hasDraft(self):
        sql = "SELECT target_id,name from draft_company_project where `status`=0 and  target_id = %s  ;" % (
            self.project_id)
        sql_result = Mysql(self.db).select(sql)
        # print(sql)
        if sql_result:
            print("待审核资料：√")
            draft = {"draft": "yes"}
        else:
            print("待审核资料：×")
            draft = {"draft": "no"}
        return draft

    def hasContact(self):
        sql = "SELECT count(distinct id)  from pms_company_project_contact where  project_id = %s  ;" % (
            self.project_id)
        sql_result = Mysql(self.db).select(sql)
        if sql_result:
            print("联系人:{}个".format(sql_result[0][0]))
            contact = {"contact": sql_result[0][0]}

        else:
            print("联系人:×")
            contact = {"contact": 0}
        return contact

    def hasFinancing(self):  # 融资历史
        sql = "SELECT count(district f.id)" \
              " from pms_company_financing f inner join pms_company_project p " \
              "on p.company_id = f.company_id and p.id  = %s  ;" % self.project_id
        sql_result = Mysql(self.db).select(sql)
        if sql_result:
            print("融资历史：{}个".format(sql_result[0][0]))
            financing = {"financing": sql_result[0][0]}

        else:
            print("融资历史：×")
            financing = {"financing": 0}
        return financing

    def hasRoadShow(self):
        sql = "SELECT id,project_id,`status`,order_type from pms_road_show_order " \
              "where `status` =9 and  project_id  = %s;" % self.project_id
        sql_result = Mysql(self.db).select(sql)
        if sql_result:
            print("路演视频：√，订单类型：{}".format('免费' if sql_result[0][3] == 1 else '付费'))
            road_show = {
                "road_show": {"has_road_show": "yes", "order_type": ('免费' if sql_result[0][3] == 1 else '付费')}}
        else:
            print("路演视频：×")
            road_show = {"road_show": {"has_road_show": "no"}}
        return road_show

    def hasOnlineFinancing(self):
        sql = "SELECT id,project_id,`status` from pms_online_financing_order " \
              "where `status` =9 and  project_id  = %s;" % self.project_id
        sql_result = Mysql(self.db).select(sql)
        if sql_result:
            print("在融项目：√，订单类型：付费")
            online_f = {"online_financing": {"is_financing": "yes", "order_type": "付费"}}

        else:
            sql = "SELECT * from pms_company_financing_demand where `status` =1 and  project_id    = %s;" % self.project_id
            sql_result = Mysql(self.db).select(sql)
            if sql_result:
                print("在融项目：√，订单类型：免费")
                online_f = {"online_financing": {"is_financing": "yes", "order_type": "免费"}}

            else:
                print("在融项目：×")
                online_f = {"online_financing": {"is_financing": "no"}}
        return online_f


if __name__ == '__main__':
    file_1 = get_dir('data_files/user_event', '批量下线.xlsx')
    df = ReadFileAsDF(file_1, 'Sheet1')
    for d in df['项目名称']:
        i = ProjectInfo(project_id=None, name=d, db='pms_test')
        project = i.getProject()
        if project.get('code') == 0:
            project.update(i.hasDraftEntrepreneur())
            project.update(i.hasDraft())
            project.update(i.hasEntrepreneur())
            project.update(i.hasContact())
            project.update(i.hasFinancing())
            project.update(i.hasRoadShow())
            project.update(i.hasOnlineFinancing())
        data = json.dumps(project, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
        df['info'] = data
    # print(df)
    writeToExcelFile(df, file_1, sheet_name='sheet')

