from flask import Blueprint,jsonify

from flask_login import current_user  # 获取当前登录用户

posts = Blueprint('posts',__name__)

@posts.route('/collect/<int:pid>/')
def collect(pid):
    if current_user.is_favorite(pid):
        current_user.del_favorite(pid)

    else:
        current_user.add_favorite(pid)

    return jsonify({'result':'OK'})