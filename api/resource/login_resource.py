from flask import Flask, render_template, redirect, make_response, jsonify
from flask_restful import reqparse, abort, Api, Resource
from data.users import User
from data.Clans import Clan
from data import db_session

parser = reqparse.RequestParser()
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)


class LoginResource(Resource):
    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        email = args['email']
        password = args['password']
        user = session.query(User).filter(User.email == email).first()
        if not user:
            abort(404, message=f"User with {email} not found")
        if not user.check_password(password):
            abort(404, message=f"Wrong password")
        user_info = {}
        if user.clan_id != -1:
            session_2 = db_session.create_session()
            clan = session_2.query(Clan).filter(Clan.id == user.clan_id).first()
            user_info['clan_tag'] = clan.short_name
            user_info['clan_name'] = clan.name
        else:
            user_info['clan_name'] = "Not in the clan"
            user_info['clan_tag'] = ''
        user_info['image'] = user.img_src
        user_info['name'] = user.name
        user_info['email'] = user.email
        return user_info
