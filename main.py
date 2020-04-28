from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_restful import Api
from data import db_session

from data.users import User
from data.lobbys import Lobby
from data.Clans import Clan

from forms.registerform import RegisterForm
from forms.loginform import LoginForm
from forms.lobbyform import LobbyForm
from forms.clanform import ClanForm
from forms.passwordchangeform import PasswordChangeForm
from forms.findclanform import FindClanForm
from forms.changeimgsrcform import ChangeImgForm

from api.resource import users_resource
from api.resource import lobby_resource
from api.resource import login_resource

from client_beta import *

app = Flask(__name__)
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.name == form.name.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой логин уже есть")
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пользователь с таким email уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/soon')
def soon():
    return render_template('soon.html')


@app.route('/patches')
def patch():
    return render_template('patchnote.html')


@app.route('/account_info')
@login_required
def account_info():
    session = db_session.create_session()
    user = session.query(User).filter(User.id == current_user.get_id()).first()
    user_info = dict()
    if user.clan_id != -1:
        session_2 = db_session.create_session()
        clan = session_2.query(Clan).filter(Clan.id == user.clan_id).first()
        user_info['clan_tag'] = clan.short_name
        user_info['clan_name'] = clan.name
    else:
        user_info['clan_name'] = "Not in the clan"
    user_info['image'] = user.img_src
    user_info['name'] = user.name
    user_info['email'] = user.email
    user_info['is_current'] = True
    return render_template('account_info.html', user=user_info)


@app.route('/account_info/<int:user_id>')
def account_info_id(user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()
    if user is not None:
        user_info = dict()
        user_info['name'] = user.name
        user_info['email'] = user.email
        user_info['is_current'] = user_id == current_user.get_id()
        return render_template('account_info.html', user=user_info)
    return redirect('/account_info')


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def account_change_password():
    form = PasswordChangeForm()
    session = db_session.create_session()
    if form.validate_on_submit():
        user = session.query(User).filter(User.id == current_user.get_id()).first()
        if not user.check_password(form.old_password.data):
            return render_template('change_password.html', form=form, message_bool=True, message='Неправильный пароль')
        if form.new_password.data != form.new_password_again.data:
            return render_template('change_password.html', form=form, message_bool=True, message='Пароли не совпадают')
        user.set_password(form.new_password.data)
        session.commit()
        return redirect('/account_info')
    return render_template('change_password.html', form=form)


@app.route('/create_lobby', methods=['GET', 'POST'])
@login_required
def create_lobby():
    form = LobbyForm()
    session = db_session.create_session()
    if form.validate_on_submit():
        if form.size.data > 4 or form.size.data < 2:
            return render_template('create_lobby.html', form=form, message='Неверное количество игроков')
        lobby = Lobby(
            map=form.map.data,
            size=form.size.data,
            lobby_leader=current_user.get_id()
        )
        session.add(lobby)
        session.commit()
        return redirect(
            f'/lobby/join/{session.query(Lobby).filter(Lobby.lobby_leader == current_user.get_id()).first().id}')
    if session.query(Lobby).filter(Lobby.lobby_leader == current_user.get_id()).first():
        return redirect('/lobby_list')
    return render_template('create_lobby.html', form=form)


@app.route('/create_clan', methods=['GET', 'POST'])
@login_required
def create_clan():
    form = ClanForm()
    session = db_session.create_session()
    if form.validate_on_submit():
        if session.query(Clan).filter(Clan.name == form.name.data).first():
            return render_template('create_clan.html', form=form, message='Такой клан уже есть')
        clan = Clan(
            name=form.name.data,
            short_name=form.short_name.data,
            clan_leader=current_user.get_id()
        )
        session.add(clan)
        session.commit()
        return redirect(f'/clan/join/{session.query(Clan).filter(Clan.name == form.name.data).first().id}')
    return render_template('create_clan.html', form=form)


@app.route('/lobby_list')
def lobby_list():
    data_web, data_client = find_lobby()
    return render_template('lobbylist.html', data_client=data_client, data_web=data_web)


@app.route('/clan_list', methods=['GET', 'POST'])
def clan_list():
    form = FindClanForm()
    if form.validate_on_submit():
        clans = find_clan(form.name.data)
        if not clans:
            return render_template('clan_list.html', form=form, message='Нет таких кланов')
        return render_template('clan_list.html', form=form, clans=clans)
    return render_template('clan_list.html', form=form, message='Начните поиск кланов', clans=find_clan(''))


@app.route('/clan_info/<int:clan_id>')
def clan_info(clan_id):
    session = db_session.create_session()
    if not session.query(Clan).filter(Clan.id == clan_id).first():
        return redirect('/wrong_id')
    clan_data = session.query(Clan).filter(Clan.id == clan_id).first()
    clan = dict()
    clan['name'] = clan_data.name
    clan['short_name'] = clan_data.short_name
    clan['is_leader'] = clan_data.clan_leader == int(current_user.get_id())
    clan['is_joined'] = is_joined(clan_data, mode=1)
    clan['image'] = clan_data.img_src
    clan['members'] = []
    clan['id'] = clan_data.id
    for user in clan_data.clan_members.split(','):
        if user == '':
            continue
        data = session.query(User).filter(User.id == int(user.strip())).first()
        if data:
            clan['members'].append(data.name)
    clan['size'] = str(len(clan['members'])) + '/50'
    return render_template('clan_info.html', clan=clan)


@app.route('/clan/join/<int:clan_id>')
@login_required
def clan_join(clan_id):
    session = db_session.create_session()
    clan = session.query(Clan).filter(Clan.id == clan_id).first()
    if clan is None:
        return redirect('/wrong_id')
    if int(clan.clan_leader) != int(current_user.get_id()):
        members = [x.strip() for x in clan.clan_members.split(',')]
        if current_user.get_id() not in members:
            clan.clan_members += str(current_user.get_id()) + ','
    else:
        clan.clan_members = str(current_user.get_id()) + ','
    session.commit()
    leave_except(clan_id, mode=1)
    session_2 = db_session.create_session()
    session_2.query(User).filter(User.id == current_user.get_id()).first().clan_id = clan_id
    session_2.commit()
    session_2.close()
    return redirect('/clan')


@app.route('/clan/leave/<int:clan_id>')
@login_required
def clan_leave(clan_id):
    session = db_session.create_session()
    clan = session.query(Clan).filter(Clan.id == clan_id).first()
    if clan is None:
        return redirect('/wrong_id')
    if int(clan.clan_leader) != int(current_user.get_id()):
        members = [x.strip() for x in clan.clan_members.split(',')]
        if str(current_user.get_id()) in members:
            members.pop(members.index(str(current_user.get_id())))
            clan.clan_members = ','.join(members)
            session.commit()
            return redirect('/clan')
        else:
            return redirect('/clan')
    else:
        session.delete(clan)
        session.commit()
        session_2 = db_session.create_session()
        user = session_2.query(User).filter(User.id == current_user.get_id()).first()
        user.clan_id = -1
        session_2.commit()
        return redirect('/clan')


@app.route('/clan')
@login_required
def clan():
    session = db_session.create_session()
    user = session.query(User).filter(User.id == current_user.get_id()).first()
    if user.clan_id != -1:
        return redirect(f'/clan_info/{user.clan_id}')
    else:
        return redirect('/clan_list')


@app.route('/lobby/<int:lobby_id>')
@login_required
def lobby_info(lobby_id):
    session = db_session.create_session()
    lobby = session.query(Lobby).filter(Lobby.id == lobby_id).first()
    if lobby is not None:
        user = session.query(User).filter(User.id == lobby.lobby_leader).first()
        args = {'lobby_leader': user.name, 'map': lobby.map, 'is_started': lobby.is_started,
                'is_joined': is_joined(lobby), 'id': lobby.id}
        members = []
        for member in lobby.lobby_members.split(','):
            try:
                members.append(session.query(User).filter(User.id == int(member)).first().name)
            except ValueError:
                pass
        return render_template('lobby_info.html', args=args, members=members)
    else:
        return redirect('/wrong_id')


@app.route('/lobby/join/<int:lobby_id>')
@login_required
def lobby_join(lobby_id):
    session = db_session.create_session()
    lobby = session.query(Lobby).filter(Lobby.id == lobby_id).first()
    if lobby is None:
        return redirect('/wrong_id')
    if int(lobby.lobby_leader) != int(current_user.get_id()):
        members = [x.strip() for x in lobby.lobby_members.split(',')]
        if current_user.get_id() not in members:
            lobby.lobby_members += str(current_user.get_id()) + ', '
            session.commit()
    else:
        lobby.lobby_members = str(current_user.get_id()) + ', '
        session.commit()
    leave_except(lobby_id)
    return redirect('/lobby_list')


@app.route('/change_img_src/<string:mode>', methods=['GET', 'POST'])
@login_required
def change_img_src(mode):
    form = ChangeImgForm()
    session = db_session.create_session()
    if form.validate_on_submit():
        if mode == 'user':
            user = session.query(User).filter(User.id == current_user.get_id()).first()
            user.img_src = form.img_src.data
            session.commit()
        elif 'clan' in mode:
            clan = session.query(Clan).filter(Clan.id == int(mode[4])).first()
            if clan:
                clan.img_src = form.img_src.data
                session.commit()
            else:
                return redirect('/wrong_id')
        return redirect('/')
    return render_template('/change_img_src.html', form=form, h1=f'Change image for: {mode}')


@app.route('/lobby/delete/<int:lobby_id>')
@login_required
def lobby_delete(lobby_id):
    session = db_session.create_session()
    lobby = session.query(Lobby).filter(Lobby.id == lobby_id).first()
    if lobby is None:
        return redirect('/wrong_id')
    if int(current_user.get_id()) == lobby.lobby_leader:
        session.delete(lobby)
        session.commit()
    return redirect('/lobby_list')


@app.route('/lobby/leave/<int:lobby_id>')
@login_required
def lobby_leave(lobby_id):
    session = db_session.create_session()
    lobby = session.query(Lobby).filter(Lobby.id == lobby_id).first()
    if lobby is None:
        return redirect('/wrong_id')
    members = [x.strip() for x in lobby.lobby_members.split(',')]
    if int(current_user.get_id()) == lobby.lobby_leader:
        session.delete(lobby)
        session.commit()
    elif current_user.get_id() in members:
        members.pop(members.index(str(current_user.get_id())))
        lobby.lobby_members = ', '.join(members)
        session.commit()
    return redirect('/lobby_list')


@app.route('/wrong_id')
def wrong_id():
    return render_template('wrong_id.html')


def find_lobby():
    session = db_session.create_session()
    temp_data_client = []
    temp_data_website = []
    for lobby in session.query(Lobby):
        temp = {}
        temp['map'] = lobby.map
        temp['sized'] = lobby.size
        temp['leader_name'] = session.query(User).filter(User.id == lobby.lobby_leader).first().name
        temp['is_started'] = lobby.is_started
        temp['leader_id'] = str(lobby.lobby_leader)
        temp['is_joined'] = is_joined(lobby)
        temp['id'] = lobby.id

        temp_data_website.append(temp.copy())
    try:
        connect_server()
        send_data_to_server('lobby_list')
        lobby_list = recv_data_from_server().split('$')
        close_connection()
        for lobby in lobby_list:
            if lobby != '':
                lobby_data = lobby.split('%')
                temp = {}
                temp['map'] = lobby_data[2]
                temp['sized'] = lobby_data[-1]
                temp['leader_id'] = lobby_data[1]
                try:
                    temp['leader_name'] = session.query(User).filter(User.id == int(lobby_data[1])).first().name
                except ValueError:
                    temp['leader_name'] = lobby_data[1]
                temp_data_client.append(temp.copy())
    except Exception:
        pass
    return temp_data_website, temp_data_client


def find_clan(name):
    session = db_session.create_session()
    temp_data = []
    for clan in session.query(Clan).filter(Clan.name.like(f'%{name}%')):
        temp = dict()
        temp['clan_name'] = clan.name
        temp['clan_id'] = clan.id
        temp_members = []
        for user in clan.clan_members.split(','):
            if user == '':
                continue
            temp_members.append(user)
        temp['size'] = len(temp_members)
        temp_data.append(temp.copy())
    return temp_data


def leave_except(data_id, mode=0):
    session = db_session.create_session()
    if mode == 0:
        for lobby in session.query(Lobby).filter(Lobby.id != data_id):
            lobby_leave(lobby.id)
    elif mode == 1:
        for clan in session.query(Clan).filter(Clan.id != data_id):
            clan_leave(clan.id)


def is_joined(data, mode=0):
    if mode == 0:
        if data.lobby_members is not None and data.lobby_members != '':
            members = [x.strip() for x in data.lobby_members.split(', ')]
            return str(current_user.get_id()) in members
        else:
            return False
    elif mode == 1:
        if data.clan_members is not None and data.clan_members != '':
            members = [x.strip() for x in data.clan_members.split(',')]
            return str(current_user.get_id()) in members
        else:
            return False


def main():
    db_session.global_init("db/blogs.sqlite")
    # session = db_session.create_session()
    api.add_resource(users_resource.UsersListResource, '/api/users')
    api.add_resource(users_resource.UsersResource, '/api/<int:user_id>')

    api.add_resource(lobby_resource.LobbyListResource, '/api/lobby')
    api.add_resource(lobby_resource.LobbyResource, '/api/lobby/<int:lobby_id>')

    api.add_resource(login_resource.LoginResource, '/api/login')
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
