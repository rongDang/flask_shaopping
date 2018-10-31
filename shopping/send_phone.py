# -*- encoding:utf8 -*-
from twilio.rest import Client

# 利用python的twilio库来发送短信信息， 会受到网络的因素影响，只能发送短信给注册的电话，不能发送给别人
account_sid = "AC01a8257b7d362fadd3a66695c77c6faa"  # twilio 给你的 Account SID
auth_token = "7da3ebac39e31a81fee5006efd407689"     # twilio给你的Auth Token
client = Client(account_sid, auth_token)


def send_message(phone, number):
    message = client.messages.create(
        to="+86"+phone,
        from_="+12602160364",
        body="【小白商城】你的验证码是:"+str(number))


# 短信接口2，使用互亿无线触发短信接口，这里用的是python3的环境(第二手准备)
"""
# 接口类型：互亿无线触发短信接口，支持发送验证码短信、订单通知短信等。
# 账户注册：请通过该地址开通账户http://sms.ihuyi.com/register.html
# 注意事项：
# （1）调试期间，请用默认的模板进行测试，默认模板详见接口文档；
# （2）请使用APIID（查看APIID请登录用户中心->验证码短信->产品总览->APIID）及 APIkey来调用接口；
# （3）该代码仅供接入互亿无线短信接口参考使用，客户可根据实际需要自行编写；
import http.client
from urllib import parse
from random import randint
host = "106.ihuyi.com"
sms_send_uri = "/webservice/sms.php?method=Submit"

# 用户名是登录用户中心->验证码短信->产品总览->APIID
account = "C65001864"
# 密码 查看密码请登录用户中心->验证码短信->产品总览->APIKEY
password = "1e4a144f6c5c7d171365e8e625cfb315"


def send_message(phone, number):
    params = parse.urlencode(
        {'account': account, 'password': password, 'content': "您的验证码是："+str(number)+"。请不要把验证码泄露给其他人。", 'mobile': phone, 'format': 'json'})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection(host, port=80, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str


if __name__ == '__main__':
    mobile = "18807395853"
    # 必须按照下面模板来写，否则会有问题  "您的验证码是：152467。请不要把验证码泄露给其他人。"
    print(send_message(mobile, 124578))
"""