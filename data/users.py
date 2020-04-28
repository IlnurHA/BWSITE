import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_media import Image


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    clan_id = sqlalchemy.Column(sqlalchemy.Integer, default=-1)
    img_src = sqlalchemy.Column(sqlalchemy.String, default='https://cdn.discordapp.com/attachments/701343081655697449/701415895028858920/logo2.png')
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


# class UserPicture(SqlAlchemyBase, Image):
#     __tablename__ = 'user_picture'
#
#     user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('user.id'), primary_key=True)
#     user = orm.relationship('User')
