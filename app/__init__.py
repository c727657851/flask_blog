from flask import Flask,render_template
from app.views import config_buleprint
# 工厂模式 创建实例  封装一个函数，可以传入参数 即返回指定的实例
# 开发环境， 测试环境， 生产环境
from app.config import config

from app.extensions import config_extensions



def create_app(config_name):   # 传入参数，从app.config 导入config文件

    # 创建实例
    app = Flask(__name__)
    app.config.from_object(config[config_name])   # 注册到文件中，让配置文件生效
    config[config_name].init_app(app)    # 调用类方法，完成特定环境初始化
    config_extensions(app)  # db与应用完成绑定
    config_buleprint(app)

    return app
