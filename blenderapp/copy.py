from flask import Flask, request, render_template, g, url_for, redirect, session
from database import get_db
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


def get_current_user():
    user_result = None

    if 'user' in session:
        user = session['user']
        db = get_db()
        user_cur = db.execute(
                ''' select id, username, email, password, client, talent, admin
                    from users where username = ?''',
                [user]
            )
        user_result = user_cur.fetchone()

    return user_result


def all_users():
    db = get_db()
    all_users_cur = db.execute(
        '''select id, username, email, password, client, talent, admin
            from users'''
    )
    all_users = all_users_cur.fetchall()
    return all_users


def user_profile(user_id):

    db = get_db()

    user_profile_cur = db.execute(
        'select id, talent_user_id, profession, years_experience, first_name, last_name from talent_profile where talent_user_id = ?''',
        [user_id]
    )
    user_profile = user_profile_cur.fetchone()

    if user_profile:
        return user_profile
    else:
        return 'Nothing'


def profile_data():
    db = get_db()
    user_data_cur = db.execute(
        ''' select id, profession, years_experience, first_name, last_name
            from talent_profile
        '''
    )

    user_data = user_data_cur.fetchall()
    return user_data


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/register', methods=['POST', 'GET'])
def register(username='stan'):

    global user

    user = None

    not_registered = True

    if request.method == 'POST' and not_registered:

        not_registered = False

        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        usertype = request.form['usertype']

        if usertype == 'client':
            client = True
            talent = False
        else:
            client = False
            talent = True

        db = get_db()

        sql_query = 'insert into users (username, email, password, client, talent, admin) \
            values (?, ?, ?, ?, ?, ?)'

        db.execute(
            sql_query,
            [
                username,
                email,
                password,
                client,
                talent,
                False
            ]
        )

        db.commit()

        session['username'] = username

        user = get_current_user()

        return render_template(
            'register.html',
            username=username,
            not_registered=not_registered
        )

    if request.method == 'POST' and not not_registered:

        # instruct user to complete profile
        if request.args.get('username') is not None:
            username = request.args.get('username')

        db = get_db()

        user_cur = db.execute(
            'select id from users where username = ?',
            [username]
        )

        user = user_cur.fetchone()

        user_id = user['id']

        profession = request.form['profession']
        years = request.form['years']
        firstname = request.form['firstname']
        lastname = request.form['lastname']

        sql_query = 'insert into talent_profile (talent_user_id, profession, years_experience, first_name, last_name) values (?, ?, ?, ?, ?)'

        db.execute(
            sql_query,
            [int(user_id), profession, int(years), firstname, lastname]
        )

        db.commit()

        return redirect(url_for('profile', user_id=user_id))
    else:
        return render_template('register.html', not_registered=not_registered)


@app.route('/login', methods=['POST', 'GET'])
def login():

    user = get_current_user()
    error = None

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        db = get_db()

        user_cur = db.execute(
            'select id, username, email, password, client, talent, admin from users where email = ?',
            [email]
        )

        user_result = user_cur.fetchone()

        # check if user exists
        if user_result:
            # check password is correct
            if check_password_hash(user_result['password'], password):
                # create user session on successful login
                session['user'] = user_result['username']
                # return '<h1>You have successfully logged in!</h1>'
                return redirect(url_for('index'))
            else:
                error = 'The password is incorrect.'
                return '<h1>The password is incorrect!</h1>'
    if request.method == 'GET':
        return render_template('login.html', user=user, error=error)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


@app.route('/profile', methods=['POST', 'GET'])
def profile(username='stan'):

    user_id = 1
    profile = user_profile(user_id)

    if request.method == 'GET':

        if profile != 'Nothing':
            return '<h1>Hello {}!</h1>'.format(profile['first_name'])
        else:
            return '<h1>There\'s something wrong with profile {}</h1>'.format(profile)

    # user = get_current_user()

    # error = None

    # if request.method == 'GET':
    #     if user:
    #         user_id = user['id']
    #         profile = user_profile(user_id)
    #         return render_template('profile.html', profile=profile, user=user)
    #     else:
    #         return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/community')
def community():

    user = get_current_user()

    if user:
        profiles = profile_data()
        return render_template('community.html', profiles=profiles, user=user)
    return render_template('community.html', user=user)


@app.route('/users')
def users():

    user = get_current_user()

    if user:
        if user['admin'] == 1:
            users = all_users()
            return render_template('users.html', all_users=users)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, port=5002)
