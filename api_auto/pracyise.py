import json

from log.log import write_log

logger = write_log(__name__)

# 判断是否是json
import json


def is_json(response):
    try:
        json_object = json.loads(response)
    except ValueError as e:
        return False
    return True


def expect_result(response, expect):
    # 先判断期望值是什么,假如期望值不为空
    print(type(response))
    if len(expect) != 0:
        if is_json(response):
            response = response
        else:
            print('jso')
            response= response.replace("'", '"')
            response = json.dumps(response)
            print(type(response))
        print(response)

        # print('dfghj', response['timestamp'], '4567', response['data']['timestamp'])




        # if 'timestamp' in response.keys():
        #     print('dasdsad')
        #     temp = k
        #     break
        # k = k + 1
        # if (temp != -1):
        #     del response[temp]['timestamp']

        # if 'timestamp' in response.keys():
        #     del response['timestamp']

        # 如果expect值在response中查不到值
        # if response.find(expect) != -1:
        #     print('11')
        #     logger.info('11111')
        #     return True
        # else:
        #     print('22')
        #     return False

    else:
        print('33')
        return False


if __name__ == '__main__':
    response = "{'code': 0, 'msg': 'success', 'data': {'appId': 'wx31c7934513c73da4', 'nonceStr': '520865f8-6807-4540-a4eb-869a61246a50', 'signature': '8aa4b26375113b6b8c6cc2420048814101815681', 'timestamp': 1600401373}, 'timestamp': 1600401373}"
    expect = "'appId': 'wx31c7934513c73da4'"
    expect_result(response, expect)
