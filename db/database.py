# 1、导入 SQLAlchemy 部件
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 连接mysql数据库需要导入pymysql模块
import pymysql
pymysql.install_as_MySQLdb()

# 2、为 SQLAlchemy 定义数据库 URL地址
# 配置数据库地址：数据库类型+数据库驱动名称://用户名:密码@机器地址:端口号/数据库名
SQLALCHEMY_DATABASE_URL = "mysql://root:123456@localhost:3306/checkauthen"

# 3、创建 SQLAlchemy 引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 4、创建数据库会
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5、创建一个Base类declarative_base
# 稍后我们将用这个类继承，来创建每个数据库模型或类（ORM 模型）
Base = declarative_base()


# 创建依赖项
# Dependency
def get_db():
    # 我们需要每个请求有一个独立的数据库会话/连接（SessionLocal），
    # 在所有请求中使用相同的会话，然后在请求完成后关闭它。
    db = SessionLocal()
    # 我们的依赖项将创建一个新的 SQLAlchemy SessionLocal，
    # 它将在单个请求中使用，然后在请求完成后关闭它。

    return db
