import datetime
from functools import wraps
import hashlib
import secrets
import string
from flask import *
import json
import sqlite3

from markupsafe import re

from CustomError import CustomError

server = Flask(__name__)


### Database ###

def admin_login_db(username, password):
    db_connection = sqlite3.connect('localServer.db')
    cursor = db_connection.cursor()
    cursor.execute(
        "SELECT * FROM ADMINS WHERE USER = ? and PASSWORD = ?;", (username, hashlib.md5(password.encode()).hexdigest()))

    if cursor.fetchone() is not None:
        session_id = ''.join(secrets.choice(
            string.ascii_letters + string.digits) for _ in range(16))
        login_time = datetime.datetime.now()
        expire_time = login_time + datetime.timedelta(hours=2)
        cursor.execute("INSERT INTO ADMIN_SESSION VALUES (?, ?, ?, ?);",
                       (session_id, username, login_time, expire_time))
        db_connection.commit()
        db_connection.close()
        return session_id

    db_connection.close()
    raise CustomError("Invalid username or password")


def check_admin_auth_db(session_id):
    db_connection = sqlite3.connect('localServer.db')
    cursor = db_connection.cursor()
    cursor.execute(
        "SELECT * FROM ADMIN_SESSION s WHERE s.ID = ? AND s.EXPIRE_DATE > now();", (session_id,))
    return cursor.fetchone() is not None


def admin_register_db(username, password):
    db_connection = sqlite3.connect('localServer.db')
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO ADMINS VALUES (?, ?)",
                   (username, hashlib.md5(password.encode()).hexdigest()))
    db_connection.commit()
    db_connection.close()


def admin_user_register_db(username, password):
    pass


### Utilities ###

# this decorator catches and handles all exceptions
def catch_all_exceptions(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CustomError as e:
            return create_response(False, {"reason": e.message})
        except Exception as e:
            return create_response(False, {"reason": e.__class__.__name__})
    return decorated_function


def check_empty_error(input_string: string, key="an input"):
    if not input_string.strip():
        raise CustomError(key + " is empty")
    return input_string


def create_response(isSuccessful: bool, data={}):
    return json.dumps({"status": "success" if isSuccessful else "error"} | data)


def check_admin_auth(json_body):
    try:
        session_id = check_empty_error(json_body["sessionId"])
        if(not check_admin_auth_db(session_id)):
            raise CustomError("Invalid Token")
    except Exception:
        raise CustomError("Error in admin auth checking")


### Routes ###

@server.route("/api/admin/login", methods=["POST"])
@catch_all_exceptions
def admin_login():
    body_data = request.get_json()
    username = check_empty_error(body_data["username"])
    password = check_empty_error(body_data["password"])
    session_id = admin_login_db(username, password)
    return create_response(True, {"sessionId": session_id})


@server.route("/api/admin/register", methods=["POST"])
@catch_all_exceptions
def admin_register():
    body_data = request.get_json()
    username = check_empty_error(body_data["username"])
    password = check_empty_error(body_data["password"])
    admin_register_db(username, password)
    return create_response(True)


@server.route("/api/admin/user/register", methods=["POST"])
def admin_user_register():
    pass


@server.route("/api/admin/activities", methods=["POST"])
def admin_activities():
    pass


@server.route("/api/user/login", methods=["POST"])
def user_login():
    pass


@server.route("/api/user/<usr>", methods=["GET"])
def user_setting(usr):
    lights_value = request.args.get("lights")
    return "<h1>Hello, " + usr + ", " + lights_value + "</h1>"


if __name__ == '__main__':
    server.run(debug=True)
