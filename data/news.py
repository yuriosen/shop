import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class News(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'news'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    bargaining = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    photo = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')

    categories = orm.relation("Category",
                              secondary="association",
                              backref="news")
