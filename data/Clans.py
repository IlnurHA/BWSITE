import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import check_password_hash, generate_password_hash


class Clan(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'clans'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    clan_leader = sqlalchemy.Column(sqlalchemy.Integer)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)
    short_name = sqlalchemy.Column(sqlalchemy.String, default=name)
    img_src = sqlalchemy.Column(sqlalchemy.String,
                                default='https://cdn.discordapp.com/attachments/701343081655697449/701344402131386438/web_bg_rem.png')
    clan_members = sqlalchemy.Column(sqlalchemy.String)
    size = sqlalchemy.Column(sqlalchemy.Integer, default=50)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
