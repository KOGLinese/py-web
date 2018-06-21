#enconding utf-8
from flask import Flask, redirect, render_template, request, url_for, session
from exts import db
import models
from models import User,Books,Clothes,Digital,Eating
import config
from functools import wraps
from flask_admin import Admin,BaseView,expose
app = Flask(__name__)
#添加配置文件
admin = Admin(app, name=u'后台管理系统')
app.config.from_object(config)
app.config['SECRET_KEY'] = '123456'
db.init_app(app)
with app.app_context():
    db.create_all()

#登录限制装饰器
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            redirect(url_for('login'))
    return wrapper

@app.route('/')
def index():
    return render_template('index.html')  #模板

@app.route('/login/',methods =['GET','POST'])
def login():
        if request.method == 'GET':
            return render_template('login.html')
        else:
            account = request.form.get('account')
            password = request.form.get('password')
            user = User.query.filter(User.password == password, User.account == account).first()
            if user:
                #print(user.username)
                session['user_id'] = user.id
                session.permanent = True
                return redirect(url_for('index', user=user))
            else:
                return u'账号或者密码错误'


@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        account = request.form.get('account')
        username = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter(User.account == account).first()
        if user:
            return u'账号已被注册'
        else:
            if password1 != password2:
                return u'两次密码不同'
            else:
                user = User(account=account, username=username, password=password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

@app.route('/logout/')
def logout():
    #删除id
    # session.pop('user_id')
    # del session('user_id')
    session.clear()
    return redirect(url_for('login'))

@app.route('/user/<username>')
def user(username):
    user = User.query.filter(User.username == username).first()
    if user:
        return render_template('user.html', user=user)

@app.route('/books')
def books():
    context={
        'books': Books.query.all()
    }
    return render_template('book.html', **context)

@app.context_processor
def my_context_prcessor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    return {}


if __name__=='__main__':
    app.run(debug=True)

