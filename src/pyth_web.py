from datetime import datetime, timedelta
from flask import Flask
from flask.helpers import make_response
from flask import request
import jwt
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisismyflasksecretkey'


def setup_db():
    open("database.db", "w").close()
    with sqlite3.connect("database.db") as _con:
        _cursor = _con.cursor()
        _cursor.execute(
            "CREATE TABLE IF NOT EXISTS User ('id' INTEGER, 'login' TEXT, "
            "'password' TEXT, 'token' DEFAULT NULL, PRIMARY KEY ('id'))")
        _cursor.execute("INSERT OR IGNORE INTO User (id, login, password) "
                        "VALUES ('1', 'admin', 'password')")
        _cursor.execute("INSERT OR IGNORE INTO User (id, login, password) "
                        "VALUES ('2', 'john', 'doe')")
        _cursor.execute("INSERT OR IGNORE INTO User (id, login, password) "
                        "VALUES ('3', 'alice', 'bob')")
        _con.commit()


def find_user_by_login(login):
    with sqlite3.connect('database.db') as _con:
        _cursor = _con.cursor()
        _cursor.execute(
            "SELECT * FROM User WHERE login=?", (login,))
        return _cursor.fetchone()


def save_user_token(user_id, token):
    with sqlite3.connect('database.db') as _con:
        _cursor = _con.cursor()
        _cursor.execute("UPDATE User set token=? WHERE id=?", (token, user_id))
        _con.commit()


def confirm_user_token(token):
    with sqlite3.connect('database.db') as _con:
        _cursor = _con.cursor()
        _cursor.execute(
            "SELECT * FROM User WHERE token=?", (token,))
        return _cursor.fetchone()


@app.route('/login')
def login():
    auth = request.authorization

    if auth:
        user = find_user_by_login(auth.username)
        if user and auth.password == user[2]:
            token = jwt.encode({'user': auth.username, 'exp': datetime.utcnow() + timedelta(minutes=30)},
                               app.config['SECRET_KEY'])
            save_user_token(user[0], token)
            return 'token: ' + token
        return 'Could not found a user with login: ' + auth.username
    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login required'})


@app.route('/protected')
def protected():
    param_token = request.args.get("token")
    if param_token and confirm_user_token(param_token):
        return '<h1>Hello, token which is provided is correct </h1>'
    else:
        return '<h1>Hello, Could not verify the token </h1>'

if __name__ == '__main__':
    setup_db()
    app.run(debug=True)