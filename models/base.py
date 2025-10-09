from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select
from sqlalchemy.orm import Session


class BaseQuery:
    @classmethod
    def get_all(cls, db: Session):
        return db.scalars(select(cls)).all()

    @classmethod
    def get_by_id(cls, db: Session, id_: int):
        return db.scalar(select(cls).where(cls.id == id_))

    @classmethod
    def get_one(cls, db: Session, **filters):
        stmt = select(cls).filter_by(**filters)
        return db.scalar(stmt)


class Base(DeclarativeBase, BaseQuery):
    pass
