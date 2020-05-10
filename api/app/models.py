# generated 
# coding: utf-8
from sqlalchemy import CHAR, Column, Integer, TIMESTAMP, Table, text
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


t_sqlite_sequence = Table(
    'sqlite_sequence', metadata,
    Column('name', NullType),
    Column('seq', NullType)
)


class Subscriber(Base):
    __tablename__ = 'subscriber'

    id = Column(Integer, primary_key=True)
    phone = Column(CHAR(13), nullable=False)
    role_arn = Column(CHAR(50), nullable=False)
    username = Column(CHAR(50), nullable=False)
    created = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
