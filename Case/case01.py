import datetime
import time
import unittest

import requests


class ApiTest01(unittest.TestCase):

    def setUp(self) -> None:
        print('01开始执行啦！')
        # 先登录

    # @staticmethod
    # def test_ll():
    #     host = 'https://pitchhub-test.36kr.com'
    #     url_path = '/api/pms/project/search'
    #     url = host + url_path
    #     print('url是', url)
    #     headers = {"Content-Type": "application/json",
    #                "Accept-Encoding": "gzip, deflate, br",
    #                "Accept-Language": "zh-CN,zh;q=0.9",
    #                "Accept": "*/*"
    #                }
    #     res = requests.post(url=url, data={"partner_id": "web", "timestamp": int(round(time.time() * 1000)),
    #                                        "partner_version": "1.0.0",
    #                                        "param": {"keyword": "测试", "data": "", "siteId": 1, "platformId": 2}},
    #                         headers=headers)
    #     time.sleep(2)
    #     print(res)

    def test_a(self):
        print('this is test_a')

    def test_01(self):
        print('this is test_01')

    def test_02(self):
        print('this is test_02')

    def tearDown(self) -> None:
        print('01执行结束！')


if __name__ == '__main__':
    unittest.main()
