from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField  # 文本框
from wtforms.validators import Length

class PostsForm(FlaskForm):
    content = TextAreaField('',render_kw={'placeholder':'有什么新鲜事分享给大家'},validators=[Length(3,140,message='支持3-140个字')])
    submit = SubmitField('发表')

