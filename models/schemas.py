from typing import Union  # ,List
import datetime

# 1、创建初始 Pydantic模型/模式
from pydantic import BaseModel


# 1、创建初始 Pydantic模型/模式
class TransactionBase(BaseModel):
    trans_id: str
    user_id: str
    account_id: Union[str, None] = None
    request_id: str
    raw_file_name: str
    raw_file_path: str
    rst_file_name: str
    rst_file_path: str
    fail_reason: Union[str, None] = None
    reserve_char_1: Union[str, None] = None


# 1、创建初始 Pydantic模型/模式
class TransactionCreate(TransactionBase):
    pass


# 2、创建用于读取/返回的Pydantic模型/模式
class Transaction(TransactionBase):
    id: int
    is_deleted: int
    from_channel: int
    file_type: int
    service_type: int
    fee_type: int
    fail_reason: int
    status: int
    last_modify_time: datetime
    reserve_int_1: int

    class Config:
        orm_mode = True
