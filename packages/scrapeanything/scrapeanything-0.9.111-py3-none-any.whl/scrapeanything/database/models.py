'''SQLAlchemy Data Models.'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, relationship
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Numeric, Integer, Text, String, Date, DateTime, Time, Boolean, Enum, Float
from sqlalchemy import Table
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.sql import func
from sqlalchemy import orm
from sqlalchemy.sql import text
import enum

from scrapeanything.utils.types import Types

Base = declarative_base()

class Model(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now())

class View(Base):
    __abstract__ = True


##########################################################

# class User(Model):
#     __tablename__ = 'users'
#     __keys__ = 'name, surname, status'

#     name = Column(String(255))
#     surname = Column(String(255))
#     status = Column(Boolean)

#     subscriptions = relationship('Subscription', back_populates='user', lazy='joined', uselist=True)

# class Roulette(Model):
#     __tablename__ = 'roulettes'
#     __keys__ = 'name'

#     name = Column(String(255))
#     fiche_denominations = Column(String(100))
#     max_bets_per_match = Column(Integer)

#     subscriptions = relationship('Subscription', back_populates='roulette', lazy='joined', uselist=True)

# class Subscription(Model):
#     __tablename__ = 'subscriptions'
#     __keys__ = 'user.*, roulette.*'

#     username = Column(String(100))
#     password = Column(String(100))
#     net_profit = Column(Float)
#     next_selection_number = Column(Integer)

#     status = Column(Boolean)

#     total_debt = Column(Float)

#     initial_balance = Column(Float)
#     net_balance = Column(Float)

#     user_id = Column(Integer, ForeignKey('users.id'))
#     roulette_id = Column(Integer, ForeignKey('roulettes.id'))

#     user = relationship('User', back_populates='subscriptions', lazy='joined')
#     roulette = relationship('Roulette', back_populates='subscriptions', lazy='joined')