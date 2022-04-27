import os
import pymysql

pymysql.install_as_MySQLdb()
base_dir=os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "mysql://root:111111@localhost:3306/Shimoxi?charset=utf8" #数据库配置
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_RECORD_QUERIES = True
SQLALCHEMY_POOL_SIZE = 1024
SQLALCHEMY_POOL_TIMEOUT = 90
SQLALCHEMY_POOL_RECYCLE = 3
SQLALCHEMY_MAX_OVERFLOW = 1024