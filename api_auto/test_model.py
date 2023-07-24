# -*- coding: utf-8 -*-
# @Date : 2020-8-31 10:16
# for what :接口策测试模型
import json

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from config.db import Mysql

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class ApiTest(object):
    def __init__(self, method, url, headers=None, payload=None):
        self.method = method
        self.url = url
        self.payload = payload
        self.header = headers

    def method_requests(self):
        if self.method == 'GET':
            ''' get  '''
            url = self.url
            r = requests.get(url, headers=self.header, params=self.payload, verify=False)
            print(r.url)

            code = r.status_code
            try:
                result = r.json()
                time = r.elapsed.microseconds / 1000 / 1000
                return result, code, time
            except Exception as e:
                return 'error', code, e
        elif self.method == 'POST':
            ''' post  '''
            url = self.url
            payload = json.loads(self.payload)
            r = requests.post(url, headers=self.header, data=json.dumps(payload), verify=False)
            code = r.status_code
            try:
                result = r.json()
                time = r.elapsed.microseconds / 1000 / 1000
                return result, code, time
            except Exception as e:
                return 'error', code, e

        elif self.method == 'PUT':
            ''' put  '''
            url = self.url
            payload = json.loads(self.payload)
            r = requests.put(url, headers=self.header, data=json.dumps(payload), verify=False)
            code = r.status_code
            try:
                result = r.json()
                time = r.elapsed.microseconds / 1000 / 1000
                return result, code, time
            except Exception as e:
                return 'error', code, e
        else:
            print('请求格式错误')

    # 保存校验的结果
    def save_result(self, result, http_status, response_data, api_id, testTime):
        insert_sql = '''insert into test_result(result,http_status,response_data,api_id,testTime ) ''' \
                     '''values("%s",%d,"%s",%d,"%s") ''' \
                     % (result, http_status, str(response_data), api_id, testTime)
        print(insert_sql)
        Mysql('new_api_case').insert(insert_sql)

    # 比较期望值与返回值是否一致
    def expect_result(self, examine_type, response_code, response, expect='', http_expect_code=''):
        # 如果返回结果存在
        if response_code is not None:
            if response_code != 200:
                if examine_type == 'only_check_status':
                    print(int(http_expect_code))
                    if http_expect_code is not None:
                        if response_code == int(http_expect_code):
                            print('与期望的http状态一致')
                            return True
                        else:
                            print('与期望的http状态不一致')
                            return False
                    else:
                        print('未给出期望code')
                        return False
                else:
                    print('code:{}不是预期的200'.format(response_code))
                    return False
            else:
                if examine_type == 'only_check_status':
                    if int(http_expect_code) == 200:
                        print('与期望的http状态一致')
                        return True
                    else:
                        print('与期望的http状态不一致')
                        return False
                elif examine_type == 'no_check':
                    # 不需要查询数据库表
                    return True
                elif examine_type == 'Regular_check':
                    # 需要从expect表中获取期望结果
                    if expect == '':
                        print('无期望的返回结果')
                    else:
                        result = False
                        # 必包含的数据都存在才返回true
                        for e in expect:
                            e = json.dumps(e)  # list转为字符串
                            print(type(response))
                            response = json.dumps(response)  # method_requests 返回的是dict格式，转为str
                            result = response.find(e[1:-1])  # 掐头去尾 去掉{} 后的字符串再匹配
                            print(result)
                        if result == 1:
                            print('查询到了')
                            return True
                        else:
                            return False
                elif examine_type == 'json':
                    pass
                elif examine_type == 'entirely_check':
                    pass
                else:
                    print('未指定检查方式，请补充！')
        else:
            print('返回结果为空')
            return False


if __name__ == '__main__':
    response = "{'code': 0, 'msg': 'success', 'data': {'appId': 'wx31c7934513c73da4', 'nonceStr': '520865f8-6807-4540-a4eb-869a61246a50', 'signature': '8aa4b26375113b6b8c6cc2420048814101815681', 'timestamp': 1600401373}, 'timestamp': 1600401373}"
    expect = "{'appId': 'wx31c7934513c73da4'}"
