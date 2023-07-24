#!/usr/bin/env python
# -*- coding: utf-8 -*-


from api_auto.test_model import ApiTest
from log.log import write_log
from config.db import Mysql
import pymysql

logger = write_log(__name__)


def vip_main():
    #   获取测试基本物料
    #
    #  将结果与期望结果比较

    try:
        sql_base = '''select  id,name,url,method,payloads,environment,expect,execute from api_case where execute = 0 ;'''
        data = Mysql('api_auto').select(sql_base)
        # print(data)
        #   遍历所有用例，执行接口测试模型中的test方法
        for i in range(len(data)):
            id,name,url,method,payloads,environment,expect,execute = data[i]
            vip = ApiTest(method, url,  payload=payloads)
            res = vip.main()

            request_text = {
                'method': method,
                'url': url,
                'token': "2e01e0b2-0b70-40c0-9c0d-71056f207bf3",
                'request_body': payloads
            }

            #   如果test方法返回error，把code和url写到数据库中
            if res[0] == 'error':
                log_text = url + str(res[2])
                error_sql = '''update  `api_result` set code = "%s",test_log = "%s" where id = %s;''' % (
                    res[1], log_text, id)
                Mysql('api_auto').insert(error_sql)

            # 如果没有error，则获取到response，code，time。断言结果，存入数据库。
            else:
                response, code, time = res
                # response_time = round(time, 2)
                # print('response11', response)
                # print('expect', expect)

                try:
                    assert vip.expect_result(response, expect), '断言错误！'
                    response = pymysql.escape_string(str(response))

                    insert_res_sql = '''update  `api_result` set response="%s", result="%s", code="%s", test_log="%s",execute=%s where id = %s;''' % (
                        response, "通过", code, pymysql.escape_string(str(request_text)), 1, id)
                    Mysql('api_auto').insert(insert_res_sql)

                except AssertionError as e:
                    response = pymysql.escape_string(str(response))
                    assert_error_sql = '''update  `api_result` set  response="%s", result="%s", code="%s",test_log="%s",execute=%s where id = %s''' % (
                        response, e, code, pymysql.escape_string(str(request_text)), 2, id)
                    Mysql('api_auto').insert(assert_error_sql)

    except Exception as e:
        logger.warning(e)


if __name__ == '__main__':
    vip_main()
