from wtforms import StringField,SubmitField,PasswordField,BooleanField
from flask_wtf import FlaskForm

from wtforms.validators import DataRequired,Length,EqualTo,Email
from wtforms.validators import ValidationError  # 抛出输入的错误
# 导入用户表
from app.models import Users
from flask_wtf.file import FileField,FileRequired,FileAllowed   # 上传文件所用的  上传请求  上传类型
from app.extensions import photos

# 登录
class LoginForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(),Length(6,20,message="用户名长度必须是6-20位")])
    password = PasswordField('密码',validators=[DataRequired(),Length(6,20,message="密码长度必须是6-20位")])
    remember = BooleanField('记住密码')
    submit = SubmitField('登录')

# 注册
class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(6, 20, message="用户名长度必须6~20")])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 20, message="密码长度必须6~20")])
    confirm = PasswordField('确认密码', validators=[EqualTo('password', message="两次密码输入不一致")])
    email = StringField('邮箱', validators=[Email(message="请填写正确的邮箱格式")])   # 激活账号
    submit = SubmitField('立即注册')

    # 进一步验证，需要定义validate_字段名 方法

    def validate_username(self,field):   # field 代表用户的输入
        # 从数据库验证
        if Users.query.filter_by(username=field.data).first():   # 用户输入的值
            raise ValidationError('该用户名已经被注册')

    def validate_emial(self,field):
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册')

# 上传头像
class UploadForm(FlaskForm):
    icon =FileField('头像',validators=[FileRequired('请选择文件'),FileAllowed(photos,message='只能上传图片')])
    submit = SubmitField('立即上传')


# 修改密码
class RePassWord(FlaskForm):
    old_password = PasswordField('原密码', validators=[DataRequired(), Length(6, 20, message="密码长度必须6~20")])
    new_password = PasswordField('新密码', validators=[DataRequired(), Length(6, 20, message="密码长度必须6~20")])
    confirm = PasswordField('确认密码', validators=[EqualTo('new_password', message="两次密码输入不一致")])
    submit = SubmitField('确认')

# 修改邮箱
class ChangeEmail(FlaskForm):
    old_email = StringField('原邮箱',validators=[Email(message="请填写正确的邮箱格式")])
    new_email = StringField('新邮箱',validators=[Email(message="请填写正确的邮箱格式")])
    confirm = StringField('确认邮箱',validators=[EqualTo('new_email', message="两次邮箱输入不一致")])
    submit = SubmitField('确认')

# 找回密码
class RecoverPassword(FlaskForm):
    login_name = StringField('登录名',render_kw={'placeholder':'邮箱'},validators=[Email(message="请填写正确的邮箱格式")])
    code = StringField('验证码',render_kw={'placeholder':'验证码'})
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 20, message="密码长度必须6~20")])
    confirm = PasswordField('确认密码', validators=[EqualTo('password', message="两次密码输入不一致")])
    verification = SubmitField('立即修改')
# 重置密码
class RestePassword(FlaskForm):
    email = StringField('当前邮箱', validators=[Email(message="请填写正确的邮箱格式")])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 20, message="密码长度必须6~20")])
    confirm = PasswordField('确认密码', validators=[EqualTo('password', message="两次密码输入不一致")])
    submit = SubmitField('提交')
