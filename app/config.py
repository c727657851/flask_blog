import os

base_dir = os.path.abspath(os.path.dirname(__file__))
print(base_dir)

class Condfig:

    SECRET_KEY = '123456789000'  # CSRF 防止跨站伪造
    BOOTSTRAP_SERVER_LOCAL = True   # 从本地加载 bootstrap文件
# -------------------------------------------------------------------发邮件---------------
    # 邮箱服务器
    MAIL_SERVER = os.environ.get('MAIL_SERVER','smtp.qq.com')

    # 用户名
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME','727657851@qq.com')

    # 密码是授权码
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD','sdgrlcqylptpbdeg')
# ----------------------------------------------------------------------------------------
    # 头像设置
    # 上传文件
    # 上传文件的最大体积
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8M 大小

    # 图片上传位置
    UPLOADED_PHOTOS_DEST = os.path.join(base_dir,'static/uploads')
# -----------------------------------------------------------------------------------------

    # 只有类可以调用,初始化特定的环境
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Condfig):
    DB_USERNAME = 'root'
    DB_PASSWORD = 'czh727657851'
    DB_HOST = '127.0.0.1'
    DB_NAME = 'flask_blog_data'
    DB_PORT = '3306'
    DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT,
                                                                     DB_NAME)
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATION = False  # 触发信号


class TestingConfig(Condfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir,'bbs-testing.sqlite')
    SQLALCHEMY_TRACK_MODIFICATION = False  # 触发信号

class ProductionConfig(Condfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir,'bbs-production.sqlite')
    SQLALCHEMY_TRACK_MODIFICATION = False  # 触发信号


config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    'default':DevelopmentConfig
}