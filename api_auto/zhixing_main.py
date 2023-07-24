import json

# 处理接口期望的返回结果
from config.db import Mysql, logger


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
                    # print(type(value))

                expect_dict = {name: value}
                expect_list.append(expect_dict)
            else:
                print('无需要校验的参数')
        if expect_list:
            return expect_list
        else:
            return False

    except Exception as e:
        logger.warning(e)
        return False


if __name__ == '__main__':
    get_api = get_api_expect_response(1)
    for i in get_api:
        print(i)
        print(type(i))

        i = json.dumps(i)
        print(i)

        print(type(i))

