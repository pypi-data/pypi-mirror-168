from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import time

# 创建数据库实例
app = Flask(__name__)
# url的格式为：数据库的协议：//用户名：密码@ip地址：端口号（默认可以不写）/数据库名
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Aiuser@123@172.21.17.237:3306/el"
# 动态追踪数据库的修改. 性能不好. 且未来版本中会移除. 目前只是为了解决控制台的提示才写的
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True
# 数据库对象
db = SQLAlchemy(app)


# 创建 b_data 表 实体类
class Create(db.Model):
    __tablename__ = "elel"
    Id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    host = db.Column(db.String(200), nullable=False, default='')
    user = db.Column(db.String(200), nullable=False, default='')
    password = db.Column(db.String(1000), nullable=False, default='')
    port = db.Column(db.BIGINT(), nullable=False, default='')
    datetime = db.Column(db.DateTime, nullable=False, default='')


# if __name__ == '__main__':
#     print('----------------开始搭建mysql----------------')
#     db.create_all()
#     d1 = Create()
#     db.session.commit()
#     print('----------------mysql搭建完成----------------')
