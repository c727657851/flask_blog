from .posts import Posts
from .users import Users
from app.extensions import db

# 添加用户与帖子的收藏中间关系表

collections = db.Table('collections',
                       db.Column('user_id', db.Integer, db.ForeignKey("users.id")),
                       db.Column('posts_id', db.Integer, db.ForeignKey("posts.id")),
                       )
