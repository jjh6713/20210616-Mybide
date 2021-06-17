from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class UserCreateForm(FlaskForm):
    id = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    name = StringField('이름', validators=[DataRequired(), Length(min=2, max=25)])
    age = StringField('나이', validators=[DataRequired(), Length(min=2, max=25)])
    sex = StringField('성별', validators=[DataRequired(), Length(min=1, max=25)])
    address = StringField('주소', validators=[DataRequired(), Length(min=1, max=25)])
    create_date = datetime.now()


class UserLoginForm(FlaskForm):
    id = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])

class ImageUploadForm(FlaskForm):
    tag = StringField('태그', validators=[DataRequired()])