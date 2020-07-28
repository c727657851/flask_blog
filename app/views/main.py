from flask import Blueprint, render_template, redirect,url_for,flash,request  # 导入蓝本
from app.forms import PostsForm
from flask_login import current_user
from app.models import Posts
from app.extensions import db

main = Blueprint('main', __name__)

@main.route('/',methods=['GET','POST'])
def index():
    # 发表
    form = PostsForm()


    if form.validate_on_submit():
        # 用户想发表内容必须先登录  并且获取当前登录用户名
        if current_user.is_authenticated:
            # 获取该用户对象
            u = current_user._get_current_object()
            p = Posts(content=form.content.data,user=u)
            db.session.add(p)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('请先登录')
            return redirect(url_for('users.login'))

    # posts = Posts.query.filter_by(rid=0).all()  # 获取发表的内容
    # 获取用户查看第几页
    page = request.args.get('page',1,type=int)

    #
    pagination = Posts.query.filter_by(rid=0).order_by(Posts.timestamp.desc()).paginate(page, per_page=5,error_out=False)
    posts = pagination.items  # 当前对象的所有数据

    return render_template('main/index.html',form=form,posts=posts,pagination=pagination)


