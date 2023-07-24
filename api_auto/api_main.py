import time

from api_auto.test_model import ApiTest
from config.db import Mysql
import logging

logger = logging.getLogger('log')


# Create your views here.
def get_api_info(project_id):
    try:

        # 查询api_info
        sql_api_info = "select id,api_path,method,request_parameter_type,examine_type,http_expect_code" \
                       " from api_info where project_id=%d ;" % project_id
        api_info = Mysql('new_api_case').select(sql_api_info)

        return api_info
    except Exception as e:
        logger.warning(e)
        return False


# 获取接口对应的header
def get_api_head(api_id):
    try:
        # 查询api_head
        sql_api_head = "select name,value" \
                       " from api_head where api_id=%d ;" % api_id
        api_head = Mysql('new_api_case').select(sql_api_head)

        return api_head
    except Exception as e:
        logger.warning(e)
        return False


# 获取接口对应的请求参数
def get_api_parameter(api_id):
    try:

        # 查询api_parameter
        sql_api_parameter = "select name,value" \
                            " from api_parameter where api_id=%d ;" % api_id
        api_parameter = Mysql('new_api_case').select(sql_api_parameter)

        return api_parameter
    except Exception as e:
        logger.warning(e)
        return False


# 获取接口对应的请求参数raw
def get_api_parameter_raw(api_id):
    try:

        # 查询api_parameter_raw
        sql_api_parameter_raw = "select data" \
                                " from api_parameter_raw where api_id=%d ;" % api_id
        api_parameter_raw = Mysql('new_api_case').select(sql_api_parameter_raw)

        return api_parameter_raw
    except Exception as e:
        logger.warning(e)
        return False


# 处理接口期望的返回结果
def get_api_expect_response(api_id):
    try:

        # 查询api_expect_response
        sql_api_expect_response = "select name,value,_type,required" \
                                  " from api_expect_response where api_id=%d ;" % api_id
        api_expect_response = Mysql('new_api_case').select(sql_api_expect_response)
        expect_list = []
        for e in range(len(api_expect_response)):
            name = api_expect_response[e][0]
            value = api_expect_response[e][1]
            _type = api_expect_response[e][2]
            required = api_expect_response[e][3]
            if required == 1:
                if _type == 'Int':
                    value = int(value)
                    print(type(value))

                expect_dict = {name: value}
                expect_list.append(expect_dict)
            else:
                print('无需要校验的参数')
        if expect_list:
            print(type(expect_list))
            return expect_list
        else:
            return False

    except Exception as e:
        logger.warning(e)
        return False


def api_main(project_id):
    api_info = get_api_info(project_id)
    print(api_info)
    if api_info == '':
        print('无可执行的接口api_info')
        return '无可执行的接口api_info'
    elif api_info == '查询失败':
        print('查询失败')
        return '查询失败'
    else:
        for a in range(len(api_info)):
            id, api_path, method, request_parameter_type, examine_type, http_expect_code = api_info[a]
            print('id:{},api_path:{},http_expect_code:{}'.format(id, api_path, http_expect_code))
            # 获取headers
            api_headers = get_api_head(id)
            if api_headers == '':
                print('id={}接口未配置headers'.format(id))
                headers = None
            elif api_headers == '查询失败':
                break
            else:
                headers = {}
                for h in range(len(api_headers)):
                    name, value = api_headers[h]
                    headers = {name: value}
                    print(type(headers))
                    # headers = json.dumps(headers)
                    print('headers:{}'.format(headers))

            # 检查请求参数的格式，如果是form_data，则从api_parameter表查询
            if request_parameter_type == 'form-data':
                api_parameter = get_api_parameter(id)
                if api_parameter == '':
                    print('id={}接口无参数'.format(id))
                    paras = None
                elif api_parameter == '查询失败':
                    break
                else:
                    paras = {}
                    for p in range(len(api_parameter)):
                        name, value = api_parameter[p]
                        # print('name:{},value:{}'.format(name, value))
                        paras = {name: value}
                        print('paras:{}'.format(paras))

            #  从api_parameter_raw查询
            elif request_parameter_type == 'raw':
                api_parameter = get_api_parameter_raw(id)
                if api_parameter == '':
                    print('id={}接口未配置请求参数'.format(id))
                    paras = None
                elif api_parameter == '查询失败':
                    break
                else:

                    # print('乐行', api_parameter)
                    paras = api_parameter[0][0]
                    # print(paras)
            else:
                pass

            # 请求接口
            api = ApiTest(method=method, url=api_path, headers=headers, payload=paras)
            res = api.method_requests()
            result, code, use_time = res
            # print(res)
            #     检查结果是否符合预期
            # 先获取预期结果

            """
            校验返回的结果是否符合预期
            """
            # 检查校验的时间
            testTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 获取期望值
            expect = get_api_expect_response(id)
            print(expect)
            # 调用比较函数比较
            cp = api.expect_result(examine_type=examine_type, response_code=code, response=result, expect=expect,
                                   http_expect_code=http_expect_code)
            if cp:
                pass_or_not = 'pass'
            else:
                pass_or_not = 'fail'
            api.save_result(result=pass_or_not, http_status=code, response_data=result, api_id=id, testTime=testTime)


if __name__ == '__main__':
    api = api_main(1)
