
# 所有的扩展都存放这里面，通过导入这个文件到app/__init__.py文件使用

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_login import LoginManager
from flask_uploads import UploadSet,IMAGES   # 上传设置 IMAGES 只能上传图片
from flask_uploads import configure_uploads,patch_request_class  # 上传文件初始化
from flask_moment import Moment  # 时间处理

# 创建对象
db = SQLAlchemy()
migrate = Migrate(db=db)
bootstrap = Bootstrap()
mail = Mail()
login_manager = LoginManager()
photos = UploadSet('photos',IMAGES)
moment = Moment()

# 封装一个方法  用来跟app 完成绑定

def config_extensions(app):
    db.init_app(app)  # 初始化实例
    migrate.init_app(app)  # 绑定
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)   # 登录初始化
    login_manager.login_message = '只有登录才可以访问'
    login_manager.login_view = 'users.login'  # 登录视图函数，没有登录跳转到这里
    login_manager.session_protection = 'strong'   # None strong 最严格的保护 basic最基本的保护

    # 上传文件初始化
    configure_uploads(app,photos)   # 与app绑定

    # 让上传文件配置生效  上传的大小和上传的位置
    patch_request_class(app,size=None)   # 如果为None 使用config中的设置  默认64M，最大就是自己设置的8M



