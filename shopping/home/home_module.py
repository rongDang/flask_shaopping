# -*- encoding:utf8 -*-
import datetime, json, math, os, time
from shopping.SQL import SQL
from flask import Blueprint, render_template, request, url_for, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from ..pay import buy
home = Blueprint("home", __name__, url_prefix="/home", template_folder="templates", static_folder="static")


@home.route("/index")
def index():
    name = session.get("ID")
    nick_name = session.get("nick_name")
    sql = SQL("shopping_flask")
    # 首页购物车数据显示,显示5条数据
    # 从数据库中获取不同种类的商品数据,1电脑，2手机，3平板，4配件，5硬件
    result = sql.select("select * from commodity where kind='%s'" % "1")[0:8]
    result1 = sql.select("select * from commodity where kind='%s'order by Sales desc" % "2")
    result2 = sql.select("select * from commodity where kind='%s'" % "3")[0:8]
    result3 = sql.select("select * from commodity where kind='%s'" % "4")[0:8]
    result4 = sql.select("select * from commodity where kind='%s'" % "5")[0:8]
    result5 = sql.select("select * from commodity where kind='%s'order by Sales desc" % "1")
    cart = sql.select("select * from commodity, cart where commodity.shop_id=cart.shop_id and u_name='%s'" % name)[0:5]
    cart_shop = []
    for i in cart:
        # 将查询的元组数据转换为列表，放到网页上
        shop = list(i)
        cart_shop.append(shop)
    sql.close()
    return render_template("index.html", data=locals())


# 退出登录
@home.route("/logout")
def logout():
    session.clear()
    return redirect("/home/index")


# 详情页面的字体需要设置大些
@home.route("/details")
def details():
    sql = SQL("shopping_flask")
    # 获取商品id，通过id来查询商品
    id = request.args.get("id")
    # 从session中获取用户ID,昵称
    name = session.get("ID")
    nick_name = session.get("nick_name")
    # 获取商品所有数据
    result = sql.select("select * from commodity where shop_id='%s'" % id)
    # 获取店铺名，在详情页面的店家推荐中显示数据
    result1 = sql.select("select * from commodity where stores = '%s'" % result[0][2])
    # 到数据库中查找用户是否收藏了该商品
    result2 = sql.select("select * from collect_shop where u_name = '%s' and shop_id='%s'" % (name, id))
    # 店铺收藏表中查找用户是否收藏了该店铺,
    result3 = sql.select("select * from  collect_store where username='%s'and store='%s'" % (name, result[0][2]))
    # 详情页图片数据，和高清大图
    himg = result[0][8].split(",")
    imgs = result[0][9].split(",")
    # 详情页右边的瞧了又瞧，首先获取当前商品的种类，对应种类的商品上去
    kind = result[0][12]
    guess = sql.select("select * from commodity where kind='%s' order by Sales desc" % kind)[0:6]
    sql.close()
    return render_template("details.html", data=locals())


# 店铺信息
@home.route("/store")
def store():
    # 获取用户名，判断用户是否收藏了店铺
    name = session.get("ID")
    nick_name = session.get("nick_name")
    sql = SQL("shopping_flask")
    # 获取店铺名，到商品表中查找该店铺所有的商品
    store_name = request.args.get("store_name")
    result = sql.select("select * from commodity where stores = '%s'" % store_name)
    # 到店铺收藏表查找是否存在该用户和店铺名
    result1 = sql.select("select * from collect_store where username='%s' and store='%s'" % (name, store_name))
    sql.close()
    return render_template("store.html", data=locals())


# 店铺内搜索商品,和store函数几乎一样，代码重复，后续该进
@home.route("/search_store", methods=["POST"])
def search_store():
    sql = SQL("shopping_flask")
    # nick_name = session.get("nick_name")
    store_name = request.values.get("store")
    shop_name = request.values.get("shop_name")
    trade_name = "%"+shop_name+"%"
    result = sql.select("select * from commodity where titles like '%s' and stores='%s'" % (trade_name, store_name))
    # result1 = sql.select("select * from collect_store where username='%s' and store='%s'" % (name, store_name))
    sql.close()
    return json.dumps(result)


# 店铺内价格排序，第一次点击为降序(jude为false)，第二次点击为升序(jude为true)
@home.route("/price", methods=["POST"])
def price():
    sql = SQL("shopping_flask")
    flag = request.values.get("jude")
    store = request.values.get("store")
    if flag == "false":
        result = sql.select("select * from commodity where stores='%s' order by prices desc" % store)
    else:
        result = sql.select("select * from commodity where stores='%s' order by prices asc" % store)
    sql.close()
    return json.dumps(result)


# 销量的降序排序
@home.route("/sales", methods=["POST"])
def sales():
    sql = SQL("shopping_flask")
    store = request.values.get("store")
    result = sql.select("select * from commodity where stores='%s' order by Sales desc" % store)
    sql.close()
    return json.dumps(result)


# 收藏的降序排序
@home.route("/collect", methods=["POST"])
def collect():
    sql = SQL("shopping_flask")
    store = request.values.get("store")
    result = sql.select("select * from commodity where stores='%s' order by collect desc" % store)
    sql.close()
    return json.dumps(result)


# 添加商品收藏
@home.route("/add_shop", methods=["POST"])
def add_shop():
    sql = SQL("shopping_flask")
    name = session.get("ID")
    shop_id = request.values.get("shop_id")
    # 往收藏表中添加商品id
    sql.IDU("insert into collect_shop(u_name, shop_id) values('%s','%s')" % (name, shop_id))
    sql.close()
    return "1"


# 取消商品收藏
@home.route("/del_shop", methods=["POST"])
def del_shop():
    sql = SQL("shopping_flask")
    name = session.get("ID")
    shop_id = request.values.get("shop_id")
    # 删除商品收藏表中的用户收藏
    sql.IDU("delete from collect_shop where u_name='%s' and shop_id='%s'" % (name, shop_id))
    sql.close()
    return "1"


# 添加店铺收藏
@home.route("/add_store", methods=["POST"])
def add_store():
    sql = SQL("shopping_flask")
    name = session.get("ID")
    store_name = request.values.get("store_name")
    today = datetime.date.today()
    print(store_name,today)
    # 往店铺收藏表中添加对应的数据
    sql.IDU("insert into collect_store(username, store, time) values('%s','%s','%s')" % (name, store_name, str(today)))
    sql.close()
    return "1"


# 删除店铺收藏
@home.route("/del_store", methods=["POST"])
def del_store():
    sql = SQL("shopping_flask")
    name = session.get("ID")
    store_name = request.values.get("store_name")
    # 删除对应的店铺
    sql.IDU("delete from collect_store where username='%s' and store='%s'" % (name, store_name))
    sql.close()
    return "1"


# 加入购物车操作,如果购物车中有这个商品了就在原来数量上加1
@home.route("/add_cart", methods=["POST"])
def add_cart():
    name = session.get("ID")
    sql = SQL("shopping_flask")
    today = datetime.date.today()
    number = int(request.values.get("number"))
    shop_id = request.values.get("shop_id")
    # 判断购物车中是否存在该商品且没有支付
    if sql.select("select * from cart where shop_id='%s'and u_name='%s'and state='0'" % (shop_id, name)):
        sql.IDU("update cart set number=number+'%d',date='%s' where shop_id='%s'" % (number, today,shop_id))
    else:
        sql.IDU("insert into cart(shop_id, u_name, date, number)values('%s','%s','%s','%s')" % (shop_id, name, today, number))
    sql.close()
    return "1"


# 删除购物车中的某件商品
@home.route("/del_cart", methods=["POST"])
def del_cart():
    name = session.get("ID")
    sql = SQL("shopping_flask")
    shop_id = request.values.get("shop_id")
    state = request.values.get("state")
    # 判断该商品是否在交易中(state=1)， 如果在交易中则不能删除
    if state == "1":
        return "0"
    else:
        sql.IDU("delete from cart where u_name='%s'and shop_id='%s' and state='%s'" % (name, shop_id, state))
    # 这里有个问题，就是json.dumps无法序列化时间类型，就会导致is not JSON serializable 错误,切记，如果需要的时间，就将它转换为字符串
    result = sql.select("select commodity.shop_id,titles,Zimg,cart.state "
                        "from commodity, cart where commodity.shop_id=cart.shop_id and u_name='%s'" % name)[0:5]
    print(result)
    sql.close()
    return json.dumps(result)


# 取消购物车订单
@home.route("/update_cart", methods=["POST"])
def update_cart():
    name = session.get("ID")
    sql = SQL("shopping_flask")
    shop_id = request.values.get("shop_id")
    sql.IDU("update cart set state='-1' where u_name='%s' and shop_id='%s'" % (name, shop_id))
    sql.close()
    return "1"


# 个人中心页面，需要有购物车（未设计好），商品收藏，店铺收藏数据,未完成
@home.route("/vipcenter")
def my_center():
    sql = SQL("shopping_flask")
    name = session.get("ID")
    nick_name = session.get("nick_name")
    if name == "None":
        return redirect("/register/login")
    # 商品收藏表和商品表进行联查
    collect_shop = sql.select("select commodity.* from commodity,collect_shop "
                              "where collect_shop.shop_id=commodity.shop_id and collect_shop.u_name='%s'" % name)[0:5]
    collect_store = sql.select("select * from collect_store where username='%s'" % name)
    cart = sql.select("select * from commodity,cart "
                      "where cart.shop_id=commodity.shop_id and cart.u_name='%s'" % name)[0:5]
    head_img = sql.select("select chat_head from user where phone='%s'" % name)[0][0][8:]
    sql.close()
    return render_template("vipcenter.html", data=locals())


# 商品收藏页面
@home.route("/Goods_collection")
def goods_collection():
    sql = SQL("shopping_flask")
    name = session.get("ID")
    nick_name = session.get("nick_name")
    collect_shop = sql.select("select commodity.* from commodity,collect_shop "
                              "where collect_shop.shop_id=commodity.shop_id and collect_shop.u_name='%s'" % name)
    head_img = sql.select("select chat_head from user where phone='%s'" % name)[0][0][8:]
    sql.close()
    return render_template("my_collection.html", data=locals())


# 店铺收藏页面
@home.route("/my_collect_store")
def my_collect_store():
    name = session.get("ID")
    sql = SQL("shopping_flask")
    nick_name = session.get("nick_name")
    collect_store = sql.select("select * from collect_store where username='%s'" % name)
    head_img = sql.select("select chat_head from user where phone='%s'" % name)[0][0][8:]
    sql.close()
    return render_template("my_collect_store.html", data=locals())


# 购物车页面
@home.route("/my_cart")
def cart():
    name = session.get("ID")
    sql = SQL("shopping_flask")
    nick_name = session.get("nick_name")
    # 查找所有订单，待付款，订单取消的数据
    paid = sql.select(
        "select * from commodity a,cart b where a.shop_id=b.shop_id and b.u_name='%s'" % name)
    obligation = sql.select(
        "select * from commodity a,cart b where a.shop_id=b.shop_id and b.u_name='%s' and b.state='0'" % name)
    cancel = sql.select(
        "select * from commodity a,cart b where a.shop_id=b.shop_id and b.u_name='%s' and b.state='1'" % name)
    head_img = sql.select("select chat_head from user where phone='%s'" % name)[0][0][8:]
    sql.close()
    return render_template("my_cart.html", data=locals())


# 账号安全页面
@home.route("/SAM")
def SAM():
    sql = SQL("shopping_flask")
    name = session.get("ID")
    nick_name = session.get("nick_name")
    # 用户表中查找该用户是否绑定了邮箱
    email = sql.select("select email from user where phone='%s'" % name)[0][0]
    head_img = sql.select("select chat_head from user where phone='%s'" % name)[0][0][8:]
    pay_pwd = sql.select("select pay_pwd from user where phone='%s'" % name)[0][0]
    sql.close()
    return render_template("SAM.html", data=locals())


# 修改密码页面
@home.route("/passwd", methods=["GET", "POST"])
def passwd():
    name = session.get("ID")
    sql = SQL("shopping_flask")
    nick_name = session.get("nick_name")
    head_img = sql.select("select chat_head from user where phone='%s'" % name)[0][0][8:]
    # 密码修改
    if request.method == "POST":
        new_pwd = request.values.get("new_pwd")
        # 给新密码进行加密,到数据库中进行更新
        pwd = generate_password_hash(new_pwd)
        sql.IDU("update user set pwd='%s' where phone='%s'" % (pwd, name))
        return "1"
    sql.close()
    return render_template("passwd.html", data=locals())


# 支付密码页面
@home.route("/pay_pwd", methods=["GET", "POST"])
def pay_pwd():
    name = session.get("ID")
    sql = SQL("shopping_flask")
    nick_name = session.get("nick_name")
    head_img = sql.select("select chat_head from user where phone='%s'" % name)[0][0][8:]
    # 密码修改
    if request.method == "POST":
        new_pwd = request.values.get("new_pwd")
        # 给新密码进行加密,到数据库中进行更新
        pwd = generate_password_hash(new_pwd)
        sql.IDU("update user set pay_pwd='%s' where phone='%s'" % (pwd, name))
        return "1"
    sql.close()
    return render_template("pay_pwd.html", data=locals())


# 改绑电话
@home.route("/amend_phone", methods=["GET", "POST"])
def amend_phone():
    name = session.get("ID")
    sql = SQL("shopping_flask")
    nick_name = session.get("nick_name")
    head_img = sql.select("select chat_head from user where phone='%s'" % name)[0][0][8:]
    if request.method == "POST":
        new_phone = request.values.get("new_phone")
        # 电话的更改,将电话存到session中
        session["ID"] = new_phone
        sql.IDU("update user set phone='%s' where phone='%s'" % (new_phone, name))
        sql.close()
        return "1"
    return render_template("amend_phone.html", data=locals())


# 绑定邮箱
@home.route("/amend_email", methods=["GET", "POST"])
def amend_email():
    name = session.get("ID")
    sql = SQL("shopping_flask")
    nick_name = session.get("nick_name")
    head_img = sql.select("select chat_head from user where phone='%s'" % name)[0][0][8:]
    if request.method == "POST":
        new_email = request.values.get("new_email")
        sql.IDU("update user set email='%s' where phone='%s'" % (new_email, name))
        sql.close()
        return "1"
    return render_template("amend_email.html", data=locals())


# 删除所有的商品收藏
@home.route("/delete_collect_shop", methods=["POST"])
def delete_collect_shop():
    sql = SQL("shopping_flask")
    name = session.get("ID")
    sql.IDU("delete from collect_shop where u_name='%s'" % name)
    return "1"


# 删除所有的店铺收藏
@home.route("/delete_collect_store", methods=["POST"])
def delete_collect_store():
    sql = SQL("shopping_flask")
    name = session.get("ID")
    sql.IDU("delete from collect_store where username='%s'" % name)
    return "1"


# 点击不同种类获取到的数据，1电脑，2手机，3平板，4配件，5硬件
@home.route("/kind", methods=["GET", "POST"])
def kind():
    sql = SQL("shopping_flask")
    name = session.get("ID")
    nick_name = session.get("nick_name")
    kind = request.args.get("kind")
    search_data = sql.select("select * from commodity where kind='%s'" % kind)
    page = len(search_data); page_count = math.ceil(page/20)    # 数据的数量，和总页数
    # 查找对应种类销量最高的几个数据
    Sales_data = sql.select("select * from commodity where kind='%s' order by Sales limit 0,5" % kind)
    if request.method == "POST":
        kind = request.values.get("kind")
        page = int(request.values.get("page")) * 20
        result = sql.select("select * from commodity where kind='%s' limit %s,20" % (kind, page))
        return json.dumps(result)
    return render_template("search_data.html", data=locals())


# 搜索结果展示，进行搜索时如果用户登录了则将其搜索历史记录下来
@home.route("/search", methods=["GET", "POST"])
def search():
    name = session.get("ID")
    sql = SQL("shopping_flask")
    nick_name = session.get("nick_name")
    if request.method == "POST":
        shop_name = request.values.get("shop_name")
        page = int(request.values.get("page")) * 20
        trade_name = "%" + shop_name + "%"
        search_data = sql.select("select * from commodity where titles like '%s' limit %s,20" % (trade_name, page))
        return json.dumps(search_data)
    shop_name = request.args.get("shop_name")   # 获取搜索的商品名
    trade_name = "%" + shop_name + "%"
    search_data = sql.select("select * from commodity where titles like '%s'" % trade_name)
    page = len(search_data); page_count = math.ceil(page / 20)
    # 查找对应种类销量最高的几个数据
    if search_data:
        Sales_data = sql.select("select * from commodity where kind='%s' order by Sales limit 0,5" % search_data[0][-1])
    # 如果用户登录，则将用户的搜索历史存到数据库中
    if name and shop_name:
        # 在html中没有进行查重操作，所以在数据库中进行查找判断
        if sql.select("select * from user_history where user_id='%s' and history='%s'" % (name, shop_name)):
            pass
        else:
            sql.IDU("insert into user_history(user_id, history) values('%s','%s')" % (name, shop_name))
            print("存储历史")
    sql.close()
    return render_template("search_data.html", data=locals())


# 搜索结果后的销量.
@home.route("/search_sales", methods=["GET", "POST"])
def search_price():
    name = session.get("ID")
    sql = SQL("shopping_flask")
    kind = request.args.get("kind")
    nick_name = session.get("nick_name")
    if kind:
        search_data = sql.select("select * from commodity where kind='%s' order by Sales" % kind)
        sales = kind
    else:
        shop_name = request.args.get("shop_name")
        trade_name = "%" + shop_name + "%"
        search_data = sql.select("select * from commodity where titles like '%s' order by Sales" % trade_name)
        if shop_name == "":
            print("搜索为空")
            sales = "all"
        else:
            sales = shop_name
    page = len(search_data); page_count = math.ceil(page / 20)
    # 查找对应种类销量最高的几个数据
    Sales_data = sql.select("select * from commodity where kind='%s' order by Sales limit 0,5" % search_data[0][-1])
    sql.close()
    return render_template("search_data.html", data=locals())


# 这里是查找搜索后的销量排序分页数据
@home.route("/sales_sou", methods=["POST"])
def sales_sou():
    sql = SQL("shopping_flask")
    page = request.values.get("page")
    shop_name = request.values.get("shop_name")
    trade_name = "%" + shop_name + "%"
    search_data = sql.select("select * from commodity where titles like '%s' order by Sales limit %s,20" % (trade_name, int(page)*20))
    sql.close()
    return json.dumps(search_data)


# 这里是查找种类的销量排序分页数据
@home.route("/sales_kind", methods=["POST"])
def sales_kind():
    sql = SQL("shopping_flask")
    page = request.values.get("page")
    kind = request.values.get("kind")
    search_data = sql.select("select * from commodity where kind='%s' order by Sales limit %s,20" % (kind, int(page)*20))
    sql.close()
    return json.dumps(search_data)


# 查询用户的搜索历史记录
@home.route("/history", methods=["POST"])
def history():
    name = session.get("ID")
    sql = SQL("shopping_flask")
    result = sql.select("select * from user_history where user_id='%s'" % name)[0:8]
    sql.close()
    return json.dumps(result)


# 删除用户的搜索历史,
@home.route("/del_history", methods=["POST"])
def del_history():
    name = session.get("ID")
    sql = SQL("shopping_flask")
    history = request.values.get("history")
    sql.IDU("delete from user_history where user_id='%s' and history='%s'" % (name, history))
    result = sql.select("select * from user_history where user_id='%s'" % name)[0:8]
    return json.dumps(result)


# 用户的资料修改，只能修改昵称，
@home.route("/amend_data", methods=["POST", "GET"])
def amend_data():
    name = session.get("ID")
    nick_name = session.get("nick_name")
    sql = SQL("shopping_flask")
    result = sql.select("select * from user where phone='%s'" % name)
    real_name = result[0][5]
    address = result[0][6]
    birthday = str(result[0][7]).split("-")
    head_img = sql.select("select chat_head from user where phone='%s'" % name)[0][0][8:]
    sex = sql.select("select sex from user where phone='%s'" % name)[0][0]
    if request.method == "POST":
        name = session.get("ID")
        real_name = request.values.get("real_name")
        birthday = request.values.get("birthday")
        sex = request.values.get("sex")
        sql.IDU("update user set real_name='%s',birthday='%s',sex='%s' where phone='%s'" % (real_name, birthday, sex, name))
        return "1"
    return render_template("amend_data.html", data=locals())


# 定义文件上传的配置
from werkzeug.utils import secure_filename
from app import app
UPLOAD_FOLDER = "shopping/home/static/head_portrait/"  # 上传的位置,这里设置的是相对路径
ALLOWED_EXITNSIONS = set(["png", "jpg", "gif"])  # 允许的拓展名
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER  # 设置上传文件存放目录
app.config["MAX_CONTENT_LENGTH"] = 40 * 1024 * 1024  # 限制上传文件大小


# 判断文件名是否正确
def allowed_file(filename):
    # 判断文件格式,使用rsplit()从右向左寻找,lower()将字符串大写转换为小写
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXITNSIONS


# 关于上传头像，如果用户后面的更改了手机号，而后面的手机号又被重新注册，此时头像名还是原来的手机号名，
# 所以后面需要在用户更改电话时需要在数据库中和文件夹中更改图片名
@home.route("/upload", methods=["POST"])
def flask_upload():
    # request.files内容是ImmutableMultiDict([('filename', <FileStorage: 'name.PNG' ('image/png')>)])
    print("图片上传操作", request.files)
    file = request.files["file"]
    if "file" not in request.files or file.filename == "":
        # 如果没有文件, 表示上传失败
        return "0"
    # 如果file存在，且满足allowed_file()函数，则进入该函数
    if file and allowed_file(file.filename):
        # 调用”werkzeug.secure_filename()”来使文件名安全,但是会过滤中文名
        filename = secure_filename(file.filename)
        # 更换图片名为用户名+时间戳
        name = session.get("ID")
        sql = SQL("shopping_flask")
        img_name = name+str(int(time.time()))
        filename = filename.replace(filename, img_name+".jpg")
        # 先删除用户原来的图片头像，再上传新的头像
        head = sql.select("select chat_head from user where phone='%s'" % name)[0][0]
        try:
            os.remove(head)
        except Exception:
            pass
        # 把上传的图片保存到指定的目录
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        # 将用户的头像相对地址存储到数据库中
        sql.IDU("update user set chat_head='%s' where phone='%s'" % (path, name))
        print(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return "1"
    else:
        return "0"


# 支付确认页面，点击提交订单后会POST到pay链接，
@home.route("/write_pay", methods=["GET", "POST"])
def write_pay():
    name = session.get("ID")
    nick_name = session.get("nick_name")
    id = request.args.get("id")
    store = request.args.get("store")
    title = request.args.get("title")
    prices = int(request.args.get("price"))
    number = int(request.args.get("number"))
    price = int(prices/number)
    return render_template("write_pay.html", data=locals())


# 用户支付页面,先post获取数据，如果用户支付后再GET跳转到当前页面来，改变用户购物车的数据
@home.route("/pay", methods=["GET", "POST"])
def pay():
    if request.method == "POST":
        # id:id,name:name,city:city,address:address,phone:phone,title:title,prices:prices
        id = request.values.get("id")
        consignee = request.values.get("name")
        city = request.values.get("city")
        city = city.replace("-", "")
        address = request.values.get("address")
        phone = request.values.get("phone")
        prices = request.values.get("prices")
        title = request.values.get("title")
        link = buy.pay(title, prices)
        session["pay_shop_id"] = id
        # 将收货人信息暂时存到session中,如果用户购买了则将数据存到session中
        session["consignee"] = consignee
        session["city"] = city
        session["address"] = address
        session["phone"] = phone
        return json.dumps(link)
    else:
        # 如果有用户直接进入到此链接判断session中是否有支付的订单，没有则跳转到购物车页面
        if session.get("pay_shop_id"):
            print("支付成功，更改属性")
            sql = SQL("shopping_flask")
            name = session.get("ID")
            pay_shop_id = session.get("pay_shop_id")
            sql.IDU("update cart set state='1' where state='0' and u_name='%s' and shop_id='%s'" % (name, pay_shop_id))
            consignee = session.get("consignee"); city = session.get("city")
            address = session.get("address"); phone = session.get("phone")
            # 如果用户支付了，则将数据存放到用户地址表，也就是用户的收货地址
            sql.IDU("insert into user_address(user,name,province,address,phone,shop_id) values "
                    "('%s','%s','%s','%s','%s','%s')" %(name, consignee, city, address, phone, pay_shop_id))
            return redirect("/home/my_cart")
        else:
            return redirect("/home/my_cart")


# 判断用户的收货密码是否正确。
@home.route("/judge", methods=["POST"])
def judge():
    print("asdasdsad")
    name = session.get("ID")
    sql = SQL("shopping_flask")
    password = sql.IDU("select pay_pwd from user where phone='%s'" % name)[0][0]
    pay_pwd = request.values.get("pwd")
    print(pay_pwd, password)
    if password:
        if check_password_hash(password, pay_pwd):
            return "1"
        else:
            return "0"
    return "-1"


# 收货操作
@home.route("/receiving", methods=["POST"])
def receiving():
    name = session.get("ID")
    sql = SQL("shopping_flask")
    # 这个id是购物车表中对应对应商品独有的id，有这个id的话收货就不会把相同商品一起收货了。
    id = request.values.get("id")
    shop_id = request.values.get("shop_id")
    return "1"


@home.route("/modal")
def modal():
    return render_template("kkkk.html")


@home.route("/kkkk")
def kkkk():
    print("asdasdadsasd")
    return json.dumps("{}")


