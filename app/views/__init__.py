from .main import main
from .users import users
from .posts import posts


DEFAULT_BLUEPRINT = (
    (main, ''),
    (users, '/users'),
    (posts, '/posts'),
)

# 封装一个函数，完成蓝本的注册
def config_buleprint(app):
    # 注册蓝本需要 蓝本的名称和url前缀
    for blueprint, url_prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint, url_prefix=url_prefix)
