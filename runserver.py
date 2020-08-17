#-*- encoding=UTF-8 -*-
from nowstagram import app
from nowstagram import app, db
from nowstagram.models import Image, User
from flask import render_template, redirect,request,flash,url_for,get_flashed_messages,send_from_directory
import hashlib,random,uuid,os
from flask_login import login_user,logout_user,login_required,current_user

def redirect_with_msg(target, msg, category):
    if msg != None:
        flash(msg, category=category)
    return redirect(target)

@app.route('/')
def index():
    images = Image.query.order_by(db.desc(Image.id)).limit(10).all()
    return render_template('index.html', images = images)

@app.route('/image/<int:image_id>/')
def image(image_id):
    image = Image.query.get(image_id)
    if image == None:
        return redirect('/')
    return render_template('pageDetail.html', image = image)

@app.route('/image/<image_name>')
def view_image(image_name):
    return send_from_directory(app.config['UPLOAD_DIR'], image_name)

@app.route('/profile/<int:user_id>/')
@login_required
def profile(user_id):
    print "user_id",user_id
    user = User.query.get(user_id)
    print "111111"
    if user == None:
        return redirect('/')
    print "22222"
    images = Image.query.filter_by(user_id=user_id).order_by(db.desc(Image.id))
    print "3333"
    return render_template('profile.html', user = user, images = images)

@app.route('/regloginpage/')
def regloginpage(msg=''):
    for m in get_flashed_messages(with_categories=False, category_filter=['reglogin']):
        msg = msg + m
    return render_template('login.html', msg=msg, next=request.values.get('next'))

@app.route('/reg/',methods={'get', 'post'})
def reg():
    username = request.values.get('username').strip()
    print "username:",username
    print 'type(username)',type(username)
    password = request.values.get('password').strip()
    print 'type(password)',type(password)
    print "password",password

    if username == ''or password == '':
        print 22222
        return redirect_with_msg('/regloginpage/',u'用户名或密码不能为空','reglogin')
    if  User.query.filter_by(username = username).first():
        print 1111
        return redirect_with_msg('/regloginpage/',u'用户名已存在','reglogin')

    salt = ''.join(random.sample('haiugeughcnuagwhqi148916511', 5))
    m = hashlib.md5()
    m.update(password + salt)
    password = m.hexdigest()
    print 33333

    user = User(username, password, salt)
    db.session.add(user)
    db.session.commit()
    print 44444

    login_user(user)

    return redirect('/')

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login/',methods={'get', 'post'})
def login():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()
    user = User.query.filter_by(username=username).first()

    if username == ''or password == '':
        return redirect_with_msg('/regloginpage/',u'用户名或密码不能为空','reglogin')
    if  not user:
        return redirect_with_msg('/regloginpage/',u'用户名不存在','reglogin')

    m = hashlib.md5()
    m.update(password+user.slat)
    if m.hexdigest() != user.password:
        print 111111
        return redirect_with_msg('/regloginpage/', u'用户密码错误', 'reglogin')
    print 222222

    login_user(user)
    return redirect(url_for('index'))

def save_to_loacal(file, file_name):
    save_dir = app.config['UPLOAD_DIR']
    file.save(os.path.join(save_dir, file_name))
    return '/image/' + file_name

@app.route('/upload/',methods={"POST"})
def upload():
    print 'request.files',request.files
    file = request.files['file']
    print dir(file)
    print 'file.name',file.name

    file_name = str(uuid.uuid1())+'.'+'jpg'
    url = save_to_loacal(file,file_name)
    print "url:",url
    if url:
        db.session.add(Image(url,current_user.id ))
        db.session.commit()

    return redirect('/profile/{}'.format( current_user.id))

if __name__ == '__main__':
    app.run(debug=True)