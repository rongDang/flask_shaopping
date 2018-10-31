# -*- encoding:utf8 -*-
# 使用第三方 SMTP 服务发送,这里使用的是QQ的 STMP服务发送邮件
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

my_sender = '2801293031@qq.com'  # 发件人邮箱账号
my_pass = 'hqfahgmaihmydhfb'  # 发件人授权码，用于登录第三方客户端的专用密码，用于SMTP服务


# 函数对应发送的内容，收件人的邮箱
def send_mail(connect, addressee="2801293031@qq.com"):
    try:
        msg = MIMEText("你的验证码是:"+connect, 'plain', 'utf-8')
        msg['From'] = formataddr(["小白商城", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["user", addressee])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "【小白商城】验证码"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，qq的是465或587
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、授权码
        server.sendmail(my_sender, [addressee, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
        print("邮件发送成功")
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        print("邮件发送失败")



