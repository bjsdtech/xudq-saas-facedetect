from sqlalchemy import Column, Integer, String, DateTime  # , Boolean ,ForeignKey,
# from sqlalchemy.orm import relationship


# 1、从database.py导入Base类
from db.database import Base


# Transaction 继承Base类
class Transaction(Base):
    # 表名
    __tablename__ = "t_transaction"

    # 2、创建模型属性/列，使用Column来表示 SQLAlchemy 中的默认值。
    id = Column(Integer, primary_key=True, index=True)
    is_deleted = Column(Integer)
    trans_id = Column(String, unique=True)
    user_id = Column(String)
    account_id = Column(String)
    request_id = Column(String)
    from_channel = Column(Integer)
    raw_file_name = Column(String)
    file_type = Column(Integer)
    raw_file_path = Column(String)
    rst_file_name = Column(String)
    rst_file_path = Column(String)
    service_type = Column(Integer)
    fee_type = Column(Integer)
    fail_reason = Column(String)
    status = Column(Integer)
    last_modify_time = Column(DateTime)
    reserve_int_1 = Column(Integer)
    reserve_char_1 = Column(String)

    # 3、创建关系


'''

# User继承Base类
class User(Base):
    __tablename__ = "User"

'''
