from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
# import functools
import pymysql
# import base64

from plat_id import level_deid
from pybo.forms import UserCreateForm, UserLoginForm
# from pybo import db
# from pybo.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

def create_connection():
    db_database ="login"
    db_name ="admin"
    db_password ="wqend1001"
    db_url = "mybide.cutyxjtrt78p.us-east-1.rds.amazonaws.com"

    conn = pymysql.connect(host = db_url, user = db_name, passwd = db_password, db = db_database, port = 3306)
    cursor = conn.cursor()

    return conn, cursor


@bp.route('/login/', methods=('GET', 'POST'))
def login():
    login_form = UserLoginForm()
    signup_form = UserCreateForm()

    if request.method == 'POST' and (login_form.validate_on_submit() or signup_form.validate_on_submit()):
        form_name = request.form['form-name']
        conn, cursor = create_connection()
        
        if form_name == 'Sign In':
            form = login_form

            sql = "select * from users where id = %s"
            cursor.execute(sql, form.id.data)
            check_validate = cursor.fetchall()
            print(check_validate)
            print(type(check_validate))

            if len(check_validate) == 0:
                print("error!!!")
                error = "User does not exist!!"
                flash(error)
            elif not check_password_hash(check_validate[0][1], form.password.data):
                error = "Invalid password!!"
                flash(error)
            else:
                print("good!!!")
                session.clear()
                session['user_id'] = form.id.data
                return redirect(url_for('upload.render_file'))
        else:
            form = signup_form
            sql = "select * from users where id=%s"
            cursor.execute(sql, form.id.data)
            check_validate = cursor.fetchall()

            if len(check_validate) == 0:
                pwd = generate_password_hash(form.password1.data)
                temp = (form.id.data, pwd , form.name.data, form.age.data, form.sex.data, form.address.data, form.create_date)
                sql = "insert into users ( id,pwd,name,age,sex,address,created_at ) values (%s,%s,%s,%s,%s,%s,%s)"

                cursor.execute(sql, temp)
                conn.commit()

                level_deid()
                return redirect(url_for('main.index'))
            else:
                flash('User already exists.')

    return render_template('auth/login.html', login_form=login_form, signup_form=signup_form)


@bp.before_app_request
def load_logged_in_user():
    user_id = [session.get('user_id')]

    conn, cursor = create_connection()
    sql = "select * from users where id=%s"
    cursor.execute(sql, user_id)
    id_temp = cursor.fetchall()

    if user_id is None:
        g.user = None
    else:
        g.user = id_temp

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))