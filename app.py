from flask import Flask, render_template, redirect
from flask_wtf.csrf import CSRFProtect
app = Flask(__name__)
csrf = CSRFProtect(app)
from shopping.register.register_module import register
from shopping.home.home_module import home
# 在应用中注册蓝图
app.register_blueprint(register)
app.register_blueprint(home)
app.config["SECRET_KEY"] = "BD\xefK\xd7Y8\xd7\xf1g\x01A\xf0\x1a\x0c\xb5\xc1\xfem\x04^K\xe9\xb0"


@app.route('/')
def hello_world():
    return redirect("/home/index")


# 这里添加错误404页面，和500页面，
@app.errorhandler(404)
def error_404(error):
    return render_template("register/404.html")


@app.errorhandler(500)
def error_500(error):
    return render_template("register/500.html")


if __name__ == '__main__':
    app.run()
