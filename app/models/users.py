
from app.extensions import db
from werkzeug.security import generate_password_hash,check_password_hash  # 加密 解密
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer   # 生成token
from flask import current_app  # 当前实例
from app.extensions import login_manager   # 登录管理对象
from flask_login import UserMixin
from app.models.posts import Posts


class Users(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(50),unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64),unique=True)
    confirmed = db.Column(db.Boolean,default=False)
    icon = db.Column(db.String(64),default='default.png')  # 图像图片 存放路径
    # 一对多，关系写在多的一方面
    post = db.relationship('Posts', backref='user',lazy='dynamic')

    favorites = db.relationship('Posts',secondary='collections',backref=db.backref('users',lazy='dynamic'),lazy='dynamic')    # lazy='dynamic' 懒加载

    # 在开发过程中密码不可读，以及密码永不反回
    # 对外password 对内password_hash

    @property  # 把一个方法当做属性来看待
    def password(self):
        raise AttributeError('密码不可读')

    # 设置密码
    @password.setter  # 装饰器
    def password(self,password):   # password 原始密码
        self.password_hash = generate_password_hash(password)

    # 密码校验 ，先给原始密码加密，然后与数据库中的进行对比
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    # 邮箱激活
    def generate_active_token(self,expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expires_in=expires_in)
        return s.dumps({'id':self.id})

# ----------------------------------------------------------------------------------------------------------------------
    # 验证是否激活
    @staticmethod   # 静态方法，只有类可以调用
    def check_activate_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)   # 验证是否合法
        except:
            return False

        # 如果合法，就知道哪个用户需要激活
        u = Users.query.get(data.get('id'))
        if not u:
            return False

        if not u.confirmed:
            u.confirmed = True
            db.session.commit()
        return True


    # 判断用户是否收藏了指定博客
    def is_favorite(self,pid):
        # 首先查看用户收藏了哪些帖子
        favorites = self.favorites.all()

        # 对比博客是否在这个列表中
        posts = list(filter(lambda p:p.id == pid, favorites))
        if len(posts) > 0:
            return True
        return False

    # 添加收藏
    def add_favorite(self,pid):
        # 根据传过来的参数，查出帖子
        p = Posts.query.get(pid)
        # 添加到第三张表中
        self.favorites.append(p)
        db.session.commit()

    # 取消收藏
    def del_favorite(self,pid):
        # 根据传过来的参数，查出帖子
        p = Posts.query.get(pid)
        # 删除
        self.favorites.remove(p)
        db.session.commit()



# 定义一个回调函数 如果登录成功会执行这个方法  获取用户的详细信息
@login_manager.user_loader    # 加载用户id
def load_user(uid):  # 就是users表中的id
    return Users.query.get(int(uid))   # 取出用户数据，根据用户id得到信息