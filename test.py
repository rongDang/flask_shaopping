# -*- encoding:utf8 -*-
# import random
# print(random.randint(1000, 9999))

# from werkzeug.security import check_password_hash
# print(check_password_hash("pbkdf2:sha256:50000$z9GbrFfq$ca9443ab2f534427b60930040720d8394789db3c2b388544db798b42cd177808", "111111"))

# import re
# if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', "18807395853@163.com"):
#     print("asdasdasd")

# a = "18807395853"
# print(a[3:7])
# a = a.replace(a[3:7], "****")
# print(a)

import time, re
print(int(time.time()))
# https://excashier.alipaydev.com/standard/auth.htm?payOrderId=6cf7615bf9624acfac2f3a2a99b10859.00

# from shopping.pay import buy
# # print(buy.pay("测试", 45))
# print(buy.pay("玩具", 45))
# import os
# os.remove("shopping/home/static/head_portrait/18807395853.jpg")
# a = '10.jpg'
# b = a.replace(a[:-4], '18807395853')
# print(b)

# a = "shopping/home/static/head_portrait/18807395853.jpg"
# print(a.replace("shopping",""))
# print(a[8:])
a = "湖南省-长沙市-芙蓉区"
print(a.replace("-", ""))