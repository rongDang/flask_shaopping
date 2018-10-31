# -*- encoding:utf8 -*-
# -*- coding: utf-8 -*-

from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from urllib.parse import quote_plus
from urllib.parse import urlparse, parse_qs
from base64 import decodebytes, encodebytes
import json
import random


class AliPay(object):
    """
    支付宝支付接口(PC端支付接口)
    """

    def __init__(self, appid, app_notify_url, app_private_key_path,
                 alipay_public_key_path, return_url, debug=False):
        self.appid = appid
        self.app_notify_url = app_notify_url
        self.app_private_key_path = app_private_key_path
        self.app_private_key = None
        self.return_url = return_url
        with open(self.app_private_key_path) as fp:
            self.app_private_key = RSA.importKey(fp.read())
        self.alipay_public_key_path = alipay_public_key_path
        with open(self.alipay_public_key_path) as fp:
            self.alipay_public_key = RSA.importKey(fp.read())

        if debug is True:
            self.__gateway = "https://openapi.alipaydev.com/gateway.do"
        else:
            self.__gateway = "https://openapi.alipay.com/gateway.do"

    def direct_pay(self, subject, out_trade_no, total_amount, return_url=None, **kwargs):
        biz_content = {
            "subject": subject,
            "out_trade_no": out_trade_no,
            "total_amount": total_amount,
            "product_code": "FAST_INSTANT_TRADE_PAY",
            # "qr_pay_mode":4
        }

        biz_content.update(kwargs)
        data = self.build_body("alipay.trade.page.pay", biz_content, self.return_url)
        return self.sign_data(data)

    def build_body(self, method, biz_content, return_url=None):
        data = {
            "app_id": self.appid,
            "method": method,
            "charset": "utf-8",
            "sign_type": "RSA2",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.0",
            "biz_content": biz_content
        }

        if return_url is not None:
            data["notify_url"] = self.app_notify_url
            data["return_url"] = self.return_url

        return data

    def sign_data(self, data):
        data.pop("sign", None)
        # 排序后的字符串
        unsigned_items = self.ordered_data(data)
        unsigned_string = "&".join("{0}={1}".format(k, v) for k, v in unsigned_items)
        sign = self.sign(unsigned_string.encode("utf-8"))
        # ordered_items = self.ordered_data(data)
        quoted_string = "&".join("{0}={1}".format(k, quote_plus(v)) for k, v in unsigned_items)

        # 获得最终的订单信息字符串
        signed_string = quoted_string + "&sign=" + quote_plus(sign)
        return signed_string

    def ordered_data(self, data):
        complex_keys = []
        for key, value in data.items():
            if isinstance(value, dict):
                complex_keys.append(key)

        # 将字典类型的数据dump出来
        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'))

        return sorted([(k, v) for k, v in data.items()])

    def sign(self, unsigned_string):
        # 开始计算签名
        key = self.app_private_key
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(SHA256.new(unsigned_string))
        # base64 编码，转换为unicode表示并移除回车
        sign = encodebytes(signature).decode("utf8").replace("\n", "")
        return sign

    def _verify(self, raw_content, signature):
        # 开始计算签名
        key = self.alipay_public_key
        signer = PKCS1_v1_5.new(key)
        digest = SHA256.new()
        digest.update(raw_content.encode("utf8"))
        if signer.verify(digest, decodebytes(signature.encode("utf8"))):
            return True
        return False

    def verify(self, data, signature):
        if "sign_type" in data:
            sign_type = data.pop("sign_type")
        # 排序后的字符串
        unsigned_items = self.ordered_data(data)
        message = "&".join(u"{}={}".format(k, v) for k, v in unsigned_items)
        return self._verify(message, signature)


return_url = 'https://openapi.alipaydev.com/gateway.do?app_id=2016091500513777&biz_content=%7B%22' \
             'total_amount%22%3A0.01%2C%22product_code%22%3A%22FAST_INSTANT_TRADE_PAY%22%2C%22out_trade' \
             '_no%22%3A%22201702021222%22%2C%22subject%22%3A%22Iphone6+16G%22%7D&charset=utf-8&method=' \
             'alipay.trade.page.pay&notify_url=http%3A%2F%2Fprojectsedus.com%2F&return_url=http%3A%2F%2F172.' \
             '25.98.1%3A8080%2F&sign_type=RSA2&timestamp=2018-05-6+16%3A15%3A27&version=1.0&sign=ROovejoPtqJPJJy' \
             '7Cmfry7ILMFgS8h9vy3OuagWNzlg9uk60aeIIDY71bP70QlPr5L83z%2F%2B91qQ3Lan%2FJVkIe7d3RnrJnjQ8lz5LTsw3HEgxH' \
             'al8zvF5OXzRa6OoGupyD08l6V9aVyqH%2BjdU2Od6GNPdrtpmIMAVnDXzK3dS%2BqG1MWfqJkcEgshYsGm%2BMRdojrEfl4FtKrU0CM7' \
             'uGtRPRzT3RaQQy7Kv5lGxOS4bM8WbbZUsApml8e7Ut2Hv6PuAXTJe7PRQvfN02cQyV8a2MSRXYZ0Ltap4WJOxJflSvhALH2SIIdyIelb1mv' \
             'RFAkKZINgKobXNPm4Evyod%2Bb5jiQ%3D%3D'

alipay = AliPay(
    appid="2016091500516489",  # 设置签约的appid
    app_notify_url="http://projectsedus.com/",  # 异步支付通知url
    app_private_key_path=u"E:\Work\Flask-test\shopping_flask\shopping\pay\ying_yong_si_yao.txt",  # 支付私钥
    alipay_public_key_path=u"E:\Work\Flask-test\shopping_flask\shopping\pay\zhi_fu_bao_gong_yao.txt",   # 支付宝公钥
    # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    debug=True,  # 默认False,设置是否是沙箱环境，True是沙箱环境
    return_url="http://127.0.0.1:5000/home/pay"  # 同步支付通知url,支付后返回的页面
)

o = urlparse(return_url)
query = parse_qs(o.query)
processed_query = {}
ali_sign = query.pop("sign")[0]
for key, value in query.items():
    processed_query[key] = value[0]
# print(alipay.verify(processed_query, ali_sign))
ran = random.randint(0000, 9999)


def pay(title, price):
    url = alipay.direct_pay(
        subject=title,  # 订单名称
        out_trade_no="20180901" + str(ran),  # 订单号生成，一般是当前时间(精确到秒)+用户ID+随机数
        total_amount=int(price)  # 支付金额
    )
    re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
    return re_url
    # 沙箱环境下，用自己的账号是无法支付的，支付宝提供了沙箱账号、沙箱安卓App，进行测试支付


