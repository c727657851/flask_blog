# 博客模型， 映射博文的模型

from app.extensions import db    # 导入扩展文件中的db
from datetime import datetime


class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)

    # 评论帖子id
    # id   rid
    # 1     0    表示新发表的
    # 2     1    表示对第一篇帖子的评论
    rid = db.Column(db.Integer,index=True,default=0)   # index 创建索引， 默认是0
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))


