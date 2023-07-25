from sqlalchemy.orm import Session

from . import models  # , schemas


# 通过 trans_id 查询交易记录
def get_trans_by_trans_id(db: Session, trans_id: str):
    return db.query(models.Transaction)\
        .filter(models.Transaction.trans_id == trans_id)\
        .first()


def create_trans_item(db: Session, trans: models.Transaction):

    # 使用您的数据创建一个 SQLAlchemy 模型实例。
    db_trans = models.Transaction(
        is_deleted=trans.is_deleted,

        trans_id=trans.trans_id,
        user_id=trans.user_id,
        account_id=trans.account_id,
        request_id=trans.request_id,
        from_channel=trans.from_channel,
        raw_file_name=trans.raw_file_name,
        file_type=trans.file_type,
        raw_file_path=trans.raw_file_path,
        rst_file_name=trans.rst_file_name,
        rst_file_path=trans.rst_file_path,
        service_type=trans.service_type,
        status=trans.status,
        last_modify_time=trans.last_modify_time,
        fee_type=trans.fee_type
    )

    # 使用add来将该实例对象添加到您的数据库。
    db.add(db_trans)
    # 使用commit来对数据库的事务提交（以便保存它们）。
    db.commit()
    # 使用refresh来刷新您的数据库实例（以便它包含来自数据库的任何新数据，例如生成的 ID）。
    db.refresh(db_trans)
    return db_trans