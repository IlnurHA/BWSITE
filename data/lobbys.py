import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import check_password_hash, generate_password_hash


class Lobby(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'lobby'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    lobby_leader = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    lobby_members = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    map = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_started = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    size = sqlalchemy.Column(sqlalchemy.Integer, default=4)

    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    # def connected(self, user_id):
    #     if user_id not in self.users:
    #         self.users.append(user_id)
    #         return {'success': 'OK'}
    #     else:
    #         return {'ERROR': 'You are already in lobby'}
    #
    # def disconnected(self, user_id):
    #     if user_id in self.users:
    #         self.users.pop(self.users.index(user_id))
    #         return {'success': 'OK'}
    #     else:
    #         return {'ERROR': 'id not found'}

    def start_game(self):
        pass