import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Clan(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'clans'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    owner = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    messages = sqlalchemy.Column(sqlalchemy.String, nullable=True)



