from flask import Flask, render_template, redirect, make_response, jsonify
from flask_restful import reqparse, abort, Api, Resource
from data.lobbys import Lobby
from data import db_session

parser = reqparse.RequestParser()
parser.add_argument('lobby_leader', required=True)
parser.add_argument('map', required=True)
parser.add_argument('size', required=True)
parser.add_argument('is_started', required=True)
parser.add_argument('password', required=True)


def abort_if_lobby_not_found(lobby_id):
    session = db_session.create_session()
    lobby = session.query(Lobby).get(lobby_id)
    if not lobby:
        abort(404, message=f"Lobby {lobby_id} not found")


class LobbyResource(Resource):
    def get(self, lobby_id):
        abort_if_lobby_not_found(lobby_id)
        session = db_session.create_session()
        lobby = session.query(Lobby).get(lobby_id)
        return jsonify({'lobby': lobby.to_dict(
            only=('lobby_leader', 'map', 'size', 'is_started'))})

    def delete(self, lobby_id):
        abort_if_lobby_not_found(lobby_id)
        session = db_session.create_session()
        lobby = session.query(Lobby).get(lobby_id)
        session.delete(lobby)
        session.commit()
        return jsonify({'success': 'OK'})


class LobbyListResource(Resource):
    def get(self):
        session = db_session.create_session()
        lobby = session.query(Lobby).all()
        return jsonify({'lobby': [item.to_dict(
            only=('lobby_leader', 'map', 'size', 'is_started')) for item in lobby]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        lobby = Lobby(
            title=args['lobby_leader'],
            content=args['map'],
            user_id=args['size'],
            is_published=args['is_started']
        )
        session.add(lobby)
        session.commit()
        return jsonify({'success': 'OK'})
