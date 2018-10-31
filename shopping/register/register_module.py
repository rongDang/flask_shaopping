# -*- encoding:utf8 -*-
import base64, random, re
from app import csrf
from io import BytesIO
from shopping.SQL import SQL
from shopping.Code import Captcha
from shopping.send_phone import send_message
from shopping.send_Emial import send_mail
from flask import Blueprint, render_template, request, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
register = Blueprint("register", __name__, url_prefix="/register", template_folder="templates", static_folder="static")


# 登录页面
@register.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.values.get("name")
        pwd = request.values.get("pwd")
        print(name, "---", pwd)
        # 首先查找对应用户名的密码，check_password_hash把密码和数据库中的密码散列值进行匹配
        sql = SQL("shopping_flask")
        result = sql.select("select * from user where email='%s' or phone='%s'" % (name, name))
        print(result, check_password_hash(result[0][2], pwd))
        # 在这里如果用户输入的账号不存在的话则获取的数据为空，则在if判断中会有IndexError
        try:
            # 满足条件登录成功，将用户账号存到session中
            if check_password_hash(result[0][4], pwd):
                # 这里就算邮箱登录，存到session中的也是用户的电话
                session["ID"] = result[0][2]
                session["nick_name"] = result[0][1]
                return "1"
        except IndexError:
            # 思路：能进入到这里表示用户输入的账号不存在，而其他的输入都正确就只有账号输入错误，返回-1表示账号输入错误
            return "-1"
        return "0"
    img = auth_code()
    return render_template("register/login.html", data=locals())


# 注册页面
@register.route("/sign", methods=["GET", "POST"])
def sign():
    if request.method == "POST":
        username = request.values.get("username")
        phone = request.values.get("phone")
        pwd = generate_password_hash(request.values.get("pwd"))
        print(username, "---", phone, "---", pwd)
        sql = SQL("shopping_flask")
        sql.IDU("insert into user(name,phone,pwd) values ('%s','%s','%s')" % (username, phone, pwd))
        sql.close()
        return "1"
    return render_template("register/register.html")


# 忘记密码页面
@register.route("/reset")
def reset():
    img = auth_code()
    return render_template("register/reset.html", data=locals())


# 短信发送页面
@register.route("/SMS", methods=["GET", "POST"])
def SMS():
    # 获取要发送验证码的账号，判断账号是邮箱还是电话
    flag = ""
    name = str(request.values.get("name"))
    session["reset_ID"] = name      # 将要重置密码的账号放到session中以便于后需好获取
    name1 = name
    if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', name):
        # 2801293031@qq.com
        flag = "1"
        name = name.replace(name[3:-7], "****")
    else:
        flag = "0"
        name = name.replace(name[3:7], "****")
    return render_template("register/SMS.html", data=locals())


# 重置密码页面
@register.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        # 获取要重置密码的账号， 重置后将session中保存的账号删除
        ID = session.get("reset_ID")
        # 获取密码进行加密
        pwd = generate_password_hash(request.values.get("pwd"))
        sql = SQL("shopping_flask")
        sql.IDU("update user set pwd='%s' where phone='%s' or email='%s'" % (pwd, ID, ID))
        del session["reset_ID"]
        return "0"
    return render_template("register/reset_password.html")


# Ajax访问数据库是否存在账号
@register.route("/find_name", methods=["POST"])
def find_name():
    name = request.values.get("name")
    # 连接数据库，到数据库中查找是否存在账号
    db = SQL("shopping_flask")
    result = db.select("select * from user where email='%s' or phone='%s'" % (name, name))
    if result:
        return "1"
    return "0"


# Ajax判断图片验证码
@csrf.exempt
@register.route("/judge_code", methods=["POST"])
def judge_code():
    code = request.values.get("code")
    if code.lower() == session.get("code"):
        return "1"
    return "0"


# Ajax判断短信，邮箱验证码
@csrf.exempt
@register.route("/judge_message", methods=["POST"])
def judge_message():
    message = request.values.get("message")
    if message == session.get("message"):
        return "1"
    return "0"


# Ajax发送短信验证码,获取电话，生成随机验证码存到session中
@csrf.exempt
@register.route("/send_phone", methods=["POST"])
def send_phone():
    phone = request.values.get("phone")
    number = str(random.randint(100000, 999999))
    session["message"] = number
    # 调用发送短信的函数
    # send_message(phone, number)
    print("短信发送成功~", number)
    return "1"


# Ajax发送邮箱验证码，获取邮箱，随机验证码码存到session中
@csrf.exempt
@register.route("/send_email", methods=["POST"])
def send_email():
    email = request.values.get("email")
    number = str(random.randint(100000, 999999))
    session["message"] = number
    # 调用发送邮件的函数
    # send_mail(number, str(email))
    print("邮件发送成功~", number)
    return "1"


# 验证码的更新
@csrf.exempt
@register.route("/Captcha", methods=["POST"])
def auth_code():
    # 获取验证码图片和验证码值
    code, img = Captcha.gene_graph_captcha()
    buf = BytesIO()
    img.save(buf, "jpeg")
    bur_str = buf.getvalue()
    data = str(base64.b64encode(bur_str))[1:].strip("'")
    session["code"] = code.lower()      # 把验证码的值转为小写存到session中
    print(code.lower())
    return data

