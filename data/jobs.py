import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm, Integer, String, Boolean, DateTime, ForeignKey
from data.db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase, UserMixin):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey('users.id'))
    product = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                   default=datetime.datetime.now)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                 default=datetime.datetime.now)
    bargaining = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    team_leader_user = orm.relation('User')