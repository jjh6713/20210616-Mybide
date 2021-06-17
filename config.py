# import os
# from flaskext.mysql import Mysql

# BASE_DIR = os.path.dirname(__file__)

# SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
# db_path = 'userinfo.cutyxjtrt78p.us-east-1.rds.amazonaws.com'
# SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(db_path)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "dev"
