#enconding utf-8
from flask import Flask, redirect, render_template, request, url_for, session,flash
from exts import db
import models
from models import User,Books,Clothes,Digital,Eating
import config
from functools import wraps
app = Flask(__name__)
#添加配置文件
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
    session.clear()
    return redirect(url_for('login'))

@app.route('/user/<username>/')
def user(username):
    user = User.query.filter(User.username == username).first()
    if user:
        return render_template('user.html', user=user)
    else:
        return u'密码错误，请重新充值'
@app.route('/addmoney/',methods =['GET','POST'])
def addmoney():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        addmon = request.form.get('money')
        addmon = int(addmon)
        password = request.form.get('password')
        user = User.query.filter(User.id == session['user_id']).first()
        if user:
            if password == user.password and addmon > 0:
                user.money=user.money+addmon
                db.session.commit()
                return render_template('user.html', user=user)
            else:
                return u'密码错误或者充值有误'
        else:
            return render_template('login.html')

@app.route('/search/',methods=['GET','POST'])
def search():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        pass

@app.route('/books/<id>')
def judge1(id):
    if session['user_id']:
        user = User.query.filter(User.id == session['user_id']).first()
        print(user.id)
        book = Books.query.filter(Books.id == id).first()
        if book and user:
            if user.money > book.bookprice and book.book_num > 0:
                user.money = user.money-book.bookprice
                book.book_num = book.book_num-1
                db.session.commit()
                #flash(u'购买成功')
                return u'购买成功'
            elif user.money < book.bookprice:
                #flash(u'您的余额不足')
                return u'您的余额不足'
            elif book.book_num <= 0:
                #flash(u'暂无库存')
                return u'暂无库存'
    else:
        return render_template('login.html')

@app.route('/books/')
def books():
    context={
        'books': Books.query.all()
    }
    if session.get('user_id'):
        user = User.query.filter(User.id == session['user_id']).first()
        return render_template('book.html', **context, user=user)
    else:
        return redirect(url_for('login'))

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

