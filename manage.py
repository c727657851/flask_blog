from flask_script import Manager
from app import create_app
from flask_migrate import MigrateCommand

from app.models import Posts,Users
from app.extensions import db
# 调用该方法 创建实例 而不是直接导入实例
app = create_app('default')

manager = Manager(app)
manager.add_command('db',MigrateCommand)

@manager.command
def create_test_post():
    for x in range(1,200):
        content = '内容%s' % x
        author = Users.query.filter_by(id=13).first()
        post = Posts(content=content)
        post.user = author
        db.session.commit()

if __name__ == '__main__':
    manager.run()
