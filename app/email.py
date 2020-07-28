from app.extensions import mail
from flask_mail import Message
from flask import current_app,render_template  # 当前实例
from threading import Thread  # 导入多线程


# 异步发送邮件
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

# 邮件发送给谁，邮件主题，模板 网页和客户端  其他参数
def send_mail(to_name,subject,template,**kwargs):
    # 创建邮件对象

    msg = Message(subject=subject,
                  recipients=[to_name],   # 发送给谁
                  sender=current_app.config['MAIL_USERNAME'],  # 发送方
                  )

    # 网页版  打开邮件
    msg.html = render_template(template+'.html',**kwargs)

    # 终端 打开邮件
    msg.body = render_template(template+'.txt',**kwargs)

    # 发送邮件
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

    return '邮件已发送'

