from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from hypothesis.factory import db


class Transaction(db.Model):

    __tablename__ = 'transaction'

    _id = Column('id', Integer, autoincrement=True, primary_key=True)
    datetime = Column(DateTime, nullable=False)
    customer_source = Column(
        Integer, ForeignKey('customer.id'), nullable=False
    )
    customer_target = Column(
        Integer, ForeignKey('customer.id'), nullable=False
    )
    value = Column(Numeric(precision=14, scale=2), nullable=False)
    customer_source_value = Column(
        Numeric(precision=14, scale=2), nullable=False
    )
    customer_target_value = Column(
        Numeric(precision=14, scale=2), nullable=False
    )


class Customer(db.Model):

    __tablename__ = 'customer'

    _id = Column('id', Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    balance = Column(Numeric(precision=14, scale=2), nullable=False, default=0)
    payments = relationship(
        'Transaction',
        backref='customer_payer',
        foreign_keys='Transaction.customer_source',
    )
    receivedies = relationship(
        'Transaction',
        backref='customer_receiver',
        foreign_keys='Transaction.customer_target',
    )
