import datetime
import json
import random

from config.db import Mysql


def getCode(mobile):  # 手机号获取验证码
    if str(mobile).startswith('23'):
        # 获取当前时间
        h = datetime.datetime.now().hour
        mobile = str(mobile)
        code = mobile[4:8] + str(int(mobile[8:10]) + h)
        return code
    else:
        return '请注意短信'


def CreateMobile():  # 随机生成一个233开头的手机号码，同时获取他的验证码
    result = random.randint(10 ** 7, 10 ** 8 - 1)
    mobile = ''.join(['233', str(result)])
    code = getCode(mobile)
    return mobile, code


class UserInfo(object):
    def __init__(self, user_id='', nick='', mobile='', db='mus_test'):
        self.user_id = user_id
        self.nick = nick
        self.mobile = mobile
        self.db = db
        self.user_info = {"db": self.db}
        print("在'{}'环境:".format(self.db))

    # 先判断这个手机号注册36kr账号了没有
    def getInfoByMobile(self):
        code = getCode(self.mobile)
        sql = "SELECT m.user_id,m.mobile,b.nick" \
              " from mus.user_bind_mobile m left join  mus.user_info_base b  on m.user_id=b.user_id" \
              " WHERE m.mobile=%s ;" % self.mobile
        sql_result = Mysql(self.db).select(sql)
        if sql_result:
            print("手机号'{}'已经注册用户,nick是：{},user_id是：{},此时验证码是：{}".format(self.mobile,
                                                                                         sql_result[0][2],
                                                                                         sql_result[0][0],
                                                                                         code))
            user_info = {"code": 0,
                         "user": {"user_id": sql_result[0][0], "mobile": self.mobile, "nick": sql_result[0][2],
                                  "mobile_code": code}}

        else:
            user_info = {"code": 2, "msg": "手机号尚未注册".format(self.user_id),
                         "user": {"user_id": "手机号尚未注册", 'mobile': self.mobile,"nick":"",
                                  "mobile_code": code}}
        return user_info

    def getInfoByUserId(self):  # 根据user_Id查询手机号
        sql = "SELECT m.user_id,m.mobile,b.nick from user_bind_mobile m left join  user_info_base b  on " \
              "m.user_id=b.user_id WHERE m.user_id=%s ;" % self.user_id
        sql_result = Mysql(self.db).select(sql)
        print(sql)
        if sql_result:
            code = getCode(sql_result[0][1])
            print("userid'{}'的手机号是:{}\t 验证码：{}\t nick:{}".format(self.user_id, sql_result[0][1], code,
                                                                         sql_result[0][2]))
            user_info = {"code": 0,
                         "user": {"user_id": self.user_id, "mobile": sql_result[0][1], "nick": sql_result[0][2],
                                  "mobile_code": code}
                         }
        else:
            user_info = {"code": 1, "msg": "{}未绑定手机号".format(self.user_id)}
        return user_info

    def getInfoByNick(self):  # 根据昵称查询用户信息
        sql = "SELECT m.user_id,m.mobile from user_info_base b inner join user_bind_mobile m on " \
              "m.user_id=b.user_id WHERE b.nick= BINARY '%s' ;" % self.nick
        sql_result = Mysql(self.db).select(sql)
        # print(sql)
        if sql_result:
            code = getCode(sql_result[0][1])
            print('昵称‘{}’的user_id是:{}\t 手机号是:{}'.format(self.nick, sql_result[0][0], sql_result[0][1]))
            user_info = {"code": 0,
                         "user": {"user_id": sql_result[0][0], "mobile": sql_result[0][1], "nick": self.nick,
                                  "mobile_code": code}}
        else:
            user_info = {"code": 3, "msg": "该nick未查询到账号"}
        return user_info

    def reUserid(self):
        # 根据user_Id查询身份和状态，没有user_id 的先根据手机号查询到user_id，没有手机号则根据nick,有user_Id则根据user_id查询
        if self.user_id !='':
            user_info = self.getInfoByUserId()  # 查询user_id是否绑定了手机号，获取user的信息
            if user_info.get('code') == 0:
                self.user_id = user_info.get('user').get('user_id')
            else:
                self.user_id = ''
        elif self.mobile  !='':
            user_info = self.getInfoByMobile()  # 根据手机号获取userid
            if user_info.get('code') == 0:
                self.user_id = user_info.get('user').get('user_id')
            else:
                # print('该手机号尚未注册用户')
                self.user_id = ''
        elif self.nick  !='':
            user_info = self.getInfoByNick()
            if user_info.get('code') == 0:
                self.user_id = user_info.get('user').get('user_id')
            else:
                self.user_id = ''
        else:
            user_info = {"code": 999, "msg": "至少输入一个查询条件，nick 或  user_id 或 登录手机号"}
        self.user_info.update(user_info)
        return self.user_info, self.user_id


class RoleInMrs(object):
    def __init__(self, user_id, db):
        self.user_id = user_id
        self.db = db
        print("在'{}'环境，user_id：{} 在创投的数据是:".format(self.db, self.user_id))

    # 判断在创投系统中是否投资管理员
    def isInvestorManager(self):
        sql = "SELECT id,user_id,investor_id,status,mobile,FROM_UNIXTIME(create_time/1000) " \
              "certification_time from pms_investor_manager where status =0 and user_id = %s ;" % self.user_id
        sql_result = Mysql(self.db).select(sql)
        if sql_result:  # 一个投资人只有一条数据

            print("管理员：√，机构id：{}".format(sql_result[0][2]))
            i_manager = {"investor_manager": {"investor_manager": "yes", "investor_id": sql_result[0][2]}}
        else:
            print('管理员：×')
            i_manager = {"investor_manager": {"investor_manager": "no"}}
        return i_manager

    # 判断在创投系统中是否投资人
    def isInvestor(self):
        sql = "SELECT id,user_id,investor_id,status,mobile,FROM_UNIXTIME(certification_time/1000) certification_time" \
              "  from pms_investor_ivperson where user_id = %s ;" % self.user_id
        sql_result = Mysql(self.db).select(sql)
        # print(sql_result)
        if sql_result:  # 一个投资人只有一条数据
            # 判断该投资人状态
            if sql_result[0][3] == 0:
                print('投资人：×（待审核）')
                investor_info = {"investor": {"investor": "no（待审核）"}}
            elif sql_result[0][3] == 1:
                #     判断是否有提交的资料审核
                sql_1 = "SELECT user_id,investor_id FROM pms.draft_investor_ivperson " \
                        "where user_id =%s and `status` = 0 ;" % self.user_id
                sql_1_result = Mysql(self.db).select(sql_1)
                if sql_1_result:
                    print('投资人：√，资料审核：√，机构id：{}'.format(sql_1_result[0][1]))
                    investor_info = {
                        "investor": {"investor": "yes", "investor_info": "has", "investor_id": sql_1_result[0][1]}}

                else:
                    print('投资人：√，资料审核：×，机构id：{}'.format(sql_result[0][2]))
                    investor_info = {
                        "investor": {"investor": "yes", "investor_info": "no", "investor_id": sql_result[0][2]}}

            elif sql_result[0][3] == 2:
                print('投资人：×（审核拒绝）')
                investor_info = {"investor": {"investor": "no（审核拒绝）"}}

            elif sql_result[0][3] == 3:
                print('投资人：×（已解除）')
                investor_info = {"investor": {"investor": "no（已解除）"}}

            else:
                print('数据库状态不对，请在数据库中检查状态')
                investor_info = {"investor": {"investor": "wrong_status"}}
        else:
            investor_info = {"investor": {"investor": "no"}}

            print('投资人：×')
        return investor_info

    # 判断在创投系统中是否创业者
    def isEntrepreneur(self):
        sql = "SELECT id,user_id,project_id,status,mobile,FROM_UNIXTIME(update_time/1000) certification_time" \
              "  from pms_company_project_entrepreneur where user_id = %s and status=1 ;" % (self.user_id)
        sql_result = Mysql(self.db).select(sql)
        # print(sql)
        if sql_result:
            print('创业者：√，project_id：{}'.format(sql_result[0][2]))
            entrepreneur_info = {"entrepreneur": {"entrepreneur": "yes", "project_id": sql_result[0][2]}}
        else:
            #   判断是否是审核中的创业者
            # 是否认领项目审核中
            sql_claim = "select * from pms.pms_authentication_entrepreneur where user_id=%s and status=0 " % self.user_id
            sql_claim_result = Mysql(self.db).select(sql_claim)
            # print(sql_claim)
            if sql_claim_result:
                print('创业者：审核中（认领项目）')
                entrepreneur_info = {"entrepreneur": {"entrepreneur": "审核中（认领项目）"}}

            else:  # 是否入驻项目审核中
                sql_settle = "select * from pms.draft_company_project_entrepreneur where user_id=%s and status=0 " % self.user_id
                sql_settle_result = Mysql(self.db).select(sql_settle)
                if sql_settle_result:
                    print('创业者：审核中（入驻项目）')
                    entrepreneur_info = {"entrepreneur": {"entrepreneur": "审核中（入驻项目）"}}
                else:
                    print('创业者：×')
                    entrepreneur_info = {"entrepreneur": {"entrepreneur": "no"}}
        return entrepreneur_info


if __name__ == '__main__':
    # mobile, code = CreateMobile()  # 随机获取一个用户
    # print("手机号：{}\t验证码：{}".format(mobile, code))
    # u = UserInfo(user_id='', mobile=mobile)

    u = UserInfo(nick=None, user_id=5118376, mobile=None, db='mus_test')  # 查询一个用户
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
