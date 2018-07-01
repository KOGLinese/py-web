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
        else:#点击登录按钮进入post请求
            account = request.form.get('account')#从web上获得账号
            password = request.form.get('password')#从web上获得密码
            user = User.query.filter(User.password == password, User.account == account).first()#账号密码比较，得到用户信息
            if user:
                session['user_id'] = user.id #将用户信息记入session中
                session.permanent = True
                return redirect(url_for('index', user=user))#传回主页
            else:
                return u'账号或者密码错误'


@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:#post请求
        #从前端的到数据
        account = request.form.get('account')
        username = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter(User.account == account).first()#用户重复筛选
        if user:
            return u'账号已被注册'
        else:
            if password1 != password2:
                return u'两次密码不同'
            else:
                user = User(account=account, username=username, password=password1)#创建数据
                db.session.add(user)#插入到user表中
                db.session.commit()#事物提交
                return redirect(url_for('login'))#回到登录界面

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
        #从前端获得充值金额
        addmon = request.form.get('money')
        addmon = float(addmon)
        password = request.form.get('password')
        user = User.query.filter(User.id == session['user_id']).first()
        if user:
            if password == user.password and addmon > 0:
                user.money=user.money+addmon#修改数据
                db.session.commit()#事物提交
                return render_template('user.html', user=user)
            else:
                return u'密码错误或者充值有误'
        else:
            return render_template('login.html')

@app.route('/',methods=['GET','POST'])
def search():
    if request.method == 'GET':
        return render_template('login.html')
    else:#post请求
        #得到商品名称
        goodsname = request.form.get('goodsname')
        #从4个表中进行查找
        flag=0
        book = Books.query.filter(Books.bookname.like(goodsname)).all()
        if book:
            flag += 1
        clothe = Clothes.query.filter(Clothes.clothesname.like(goodsname)).all()
        if clothe:
            flag += 1
        digital = Digital.query.filter(Digital.digitalname.like(goodsname)).all()
        if digital:
            flag += 1
        eat = Eating.query.filter(Eating.eatingname.like(goodsname)).all()
        if eat:
            flag += 1
        context = {'books': book, 'clothes': clothe, 'digitals': digital, 'eats': eat}
        if session.get('user_id'):
            user = User.query.filter(User.id == session['user_id']).first()
            return render_template('search.html', **context, user=user, flag=flag)#进入search页面
        else:
            return redirect(url_for('login'))

@app.route('/books/<id>')#传入参数id
def judge1(id):
    if session.get('user_id'):#判断用户是否登录
        user = User.query.filter(User.id == session['user_id']).first()
        good = Books.query.filter(Books.id == id).first()#从数据库中查询商品
        if good and user:
            if user.money >= good.bookprice and good.book_num > 0:#数量以及价格余额判断
                user.money = user.money-good.bookprice#更新余额
                good.book_num = good.book_num-1#更新数量
                db.session.commit()#提交事务
                return u'购买成功'
            elif user.money < good.bookprice:
                return u'您的余额不足'
            elif good.book_num <= 0:
                return u'暂无库存'
    else:
        return render_template('login.html')

@app.route('/clothe/<id>')
def judge2(id):
    if session.get('user_id'):
        user = User.query.filter(User.id == session['user_id']).first()
        good = Clothes.query.filter(Clothes.id == id).first()
        if good and user:
            if user.money >= good.clotheprice and good.clothes_num > 0:
                user.money = user.money-good.clotheprice
                good.clothes_num = good.clothes_num-1
                db.session.commit()
                return u'购买成功'
            elif user.money < good.clotheprice:
                return u'您的余额不足'
            elif good.clothes_num <= 0:
                return u'暂无库存'
    else:
        return render_template('login.html')

@app.route('/digital/<id>')
def judge3(id):
    if session.get('user_id'):
        user = User.query.filter(User.id == session['user_id']).first()
        good = Digital.query.filter(Digital.id == id).first()
        if good and user:
            if user.money >= good.digitalprice and good.digital_num > 0:
                user.money = user.money-good.digitalprice
                good.clothes_num = good.digital_num-1
                db.session.commit()
                return u'购买成功'
            elif user.money < good.digitalprice:
                return u'您的余额不足'
            elif good.digital_num <= 0:
                return u'暂无库存'
    else:
        return render_template('login.html')

@app.route('/eating/<id>')
def judge4(id):
    if session.get('user_id'):
        user = User.query.filter(User.id == session['user_id']).first()
        good = Eating.query.filter(Eating.id == id).first()
        if good and user:
            if user.money >= good.eatingprice and good.eating_num > 0:
                user.money = user.money-good.eatingprice
                good.eating_num = good.eating_num-1
                db.session.commit()
                return u'购买成功'
            elif user.money < good.eatingprice:
                return u'您的余额不足'
            elif good.eating_num <= 0:
                return u'暂无库存'
    else:
        return render_template('login.html')

@app.route('/books/')
def books():
    context={
        'books': Books.query.all()#从数据库中查找所有数据
    }
    if session.get('user_id'):
        user = User.query.filter(User.id == session['user_id']).first()
        return render_template('book.html', **context, user=user)##将表单传入book界面
    else:
        return redirect(url_for('login'))

@app.route('/clothes/')
def clothes():
    context={
        'clothes': Clothes.query.all()
    }
    if session.get('user_id'):
        user = User.query.filter(User.id == session['user_id']).first()
        return render_template('clothe.html', **context, user=user)
    else:
        return redirect(url_for('login'))

@app.route('/digital/')
def digital():
    context={
        'digitals': Digital.query.all()
    }
    if session.get('user_id'):
        user = User.query.filter(User.id == session['user_id']).first()
        return render_template('digital.html', **context, user=user)
    else:
        return redirect(url_for('login'))
@app.route('/eating/')
def eating():
    context={
        'eatings': Eating.query.all()
    }
    if session.get('user_id'):
        user = User.query.filter(User.id == session['user_id']).first()
        return render_template('eating.html', **context, user=user)
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
    app.run(host='0.0.0.0', debug=True)

#host='0.0.0.0',