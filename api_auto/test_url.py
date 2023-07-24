import json

from api_auto.test_model import VipApiTest



url = 'https://v.36kr.com/api/wechat/jssdk/ticket'


data = {'app_id':'wx31c7934513c73da4'}
header = {
          "Accept": 'application/json',
          "Content-Type": "application/json",
          }

res = VipApiTest(method = 'get', url = url, payload=data)
print(res.url)
result, code, time= res.main()
print(result, code, time)

url = 'https://v.36kr.com/api/vip/user/update'

data = {
    "code": "",
    "city": "北京市",
    "company": "测试数据",
    "practice_field": "汽车出行,教育",
    "real_name": "",
    "occupation": "010100",
    "province": "北京市",
    "financing_round": "",
    "founded_at": "",
    "lnsize": "",
    "company_verify_status": 0
}

res = VipApiTest(method = 'post', url = url, payload=json.dumps(data))

print(res.url)
result, code, time= res.main()
print(result, code, time)

"""
接口地址

方法可选

参数配置

token 输入
    
"""