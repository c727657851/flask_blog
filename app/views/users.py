import uuid

from flask import Blueprint, render_template, request, flash, redirect, url_for,current_app
from app.forms import RegisterForm, LoginForm,UploadForm,RePassWord,ChangeEmail,RecoverPassword,RestePassword
from app.models import Users
from app.extensions import db,photos
from app.email import send_mail
from flask_login import login_user,logout_user,login_required,current_user  # 当前用户
import os
from PIL import Image    # 用于生成缩略图

users = Blueprint('users', __name__)

# 注册账号
@users.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if form.validate():
        u = Users(username=form.username.data, password=form.password.data, email=form.email.data)
        db.session.add(u)
        db.session.commit()
        token = u.generate_active_token()  # 直接调用获得token,邮箱的状态
        send_mail(u.email, '激活账户', 'email/activate', username=u.username, token=token)
        flash('注册成功,请点击邮件中的链接激活账号')

        # 路由重定向
        return redirect(url_for('main.index'))  # 注册成功跳转到首页蓝本名称.视图函数名称

    return render_template('users/register.html', form=form)


# 验证用户点击激活账户
@users.route('/activate/<token>/')
def activate(token):
    if Users.check_activate_token(token):
        flash('账户已激活')
        return redirect(url_for('users.login'))
    else:
        flash('激活失败，请重新激活')
        return redirect(url_for('main.index'))

# 登录
@users.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if form.validate():
        u = Users.query.filter_by(username=form.username.data).first()   # 用户名
        if not u:
            flash('该用户不存在')
        elif not u.confirmed:
            flash('该账户没有激活，请先激活')
        elif u.verify_password(form.password.data):
            login_user(u,remember=form.remember.data)   # 如果勾上记住密码， 那么有效期是14天
            flash('登录成功')
        else:
            flash('用户名或密码错误')
            return redirect(request.args.get('next') or url_for('main.index'))   # 如果url中有next参数，那么跳转到next对应的地址 否则跳转到首页

    return render_template('users/login.html', form=form)

# 退出登录
@users.route('/logout/')
def logout():
    form = LoginForm(request.form)
    logout_user()
    flash('退出登录成功')
    # 返回登录界面
    return render_template('users/login.html',form=form)

@users.route('/profile/')
@login_required  # 如果没有登录 它会跳转到登录的视图函数  url中会有next
def profile():
    return render_template('users/profile.html')

# 上传头像，视图函数
@users.route('/change_icon/',methods=['GET', 'POST'])
@login_required
def change_icon():
    form = UploadForm()
    if form.validate():
        # print(form.icon.data)   # 获得图片源
        suffix = os.path.splitext(form.icon.data.filename)[1]   # 获取文件后缀名

        # 服务器上文件名一样，后面的会覆盖前面的，采用随机生成字符串
        # 调用下面定义的random_string函数 作为函数名字
        filename = random_string() + suffix
        photos.save(form.icon.data, name=filename)   # 保存文件  第一个参数，要保存的图片的对象 第二个参数，保存下来的图片的名称

        # 图片生成缩略图
        # 第一步 打开图片
        pathname = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],filename)
        img = Image.open(pathname)
        # 第二步 重新设置尺寸
        img.thumbnail((128,128))
        # 第三步 保存
        img.save(pathname)

        # 更换图片
        if current_user.icon != 'default.png':  # 已经上传头像了
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],current_user.icon))
        current_user.icon = filename
        db.session.add(current_user)
        db.session.commit()
        flash('头像已经更换')

        # 在页面上
        img_url = photos.url(current_user.icon)  # 获取头像的地址
        # 在数据库中保存的是图片的名称

        return render_template('users/change_icon.html',img_url=img_url)
    return render_template('users/change_icon.html', form=form)
uuid

# 生成随机字符串，用于文件的名字
def random_string(length=32):
    import random
    base_str = 'zxcvbnmqwertyuiopasdfghjkl7410852963'
    return ''.join(random.choice(base_str) for i in range(length))

# 修改密码
@users.route('/change_password/',methods=['GET', 'POST'])
def change_password():
    form = RePassWord()
    if form.validate():
        u = Users.query.filter_by(username=current_user.username).first()
        if u.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            flash('密码修改成功')
            return render_template('users/profile.html')
        else:
            flash('原密码错误')
    return render_template('repassword/change_password.html',form=form)

# 修改邮箱
@users.route('/change_email/',methods=['GET', 'POST'])
def change_email():
    form = ChangeEmail()
    u = Users.query.filter_by(username=current_user.username).first()
    if form.validate():
        if u.email == form.old_email.data:
            if u.email == form.new_email.data:
                flash('新邮箱与原邮箱不能相同')
            else:
                u.confirmed = False
                current_user.email = form.new_email.data
                db.session.add(current_user)
                db.session.commit()
                token = u.generate_active_token()
                send_mail(u.email, '更改账户邮箱', 'email/change_activate', username=u.username, token=token)
                flash('请点击新邮箱中链接，完成修改')
        else:
            flash('原邮箱不正确')


    return render_template('email/change_email.html',form=form)

# 修改邮箱发送的消息，用于点击完整修改
@users.route('/change_activate/<token>/')
def change_activate(token):
    if Users.check_activate_token(token):
        flash('账户已激活,更改邮箱成功')
    else:
        flash('激活失败，邮箱更改失败')
        form = ChangeEmail()
        u = Users.query.filter_by(username=current_user.username).first()
        u.email = form.old_email.data
        u.confirmed = True
        db.session.commit()

# 找回密码   忘记密码
@users.route('/recover_password/',methods=['GET', 'POST'])
def recover_password():
    form = RecoverPassword()
    if form.validate():
        recover_login = form.login_name.data
        u = Users.query.filter_by(email=recover_login).first()
        if u:
            token = u.generate_active_token()  # 直接调用获得token,邮箱的状态
            captcha = str(uuid.uuid1())[:6]
            send_mail(u.email, '找回密码', 'email/recover_password', username=u.username, token=token,captcha=captcha)
            flash('邮件发送成功，请点击邮箱中的链接完成密码重置')

        else:
            flash('用户名或邮箱错误')

    return render_template('repassword/recover_password.html',form=form)

# 找回密码 邮件中的显示信息
@users.route('/recover_activate/<token>/',methods=['GET', 'POST'])
def recover_activate(token):
    form = RestePassword()
    if Users.check_activate_token(token):
        u = Users.query.filter_by(email=form.email.data).first()
        u.password = form.password.data
        db.session.commit(u)
        flash('找回成功')
        return redirect(url_for('users.login'))

    else:
        flash('找回失败请重新尝试')
        return redirect(url_for('repassword.recover_password'))
    return render_template('repassword/reset_password.html',form=form)