import datetime
import hashlib
import secrets
import string
from flask import *
import json
import sqlite3

from markupsafe import re

server = Flask(__name__)


### Database ###

def admin_login_db(username, password):
    db_connection = sqlite3.connect('localServer.db')
    cursor = db_connection.cursor()
    cursor.execute(
        "SELECT * FROM ADMINS WHERE USER = ? and PASSWORD = ?", (username, hashlib.md5(password.encode()).hexdigest()))
    found_admin = cursor.fetchone()

    if found_admin is not None:
        session_id = ''.join(secrets.choice(
            string.ascii_letters + string.digits) for _ in range(16))
        login_time = datetime.datetime.now()
        expire_time = login_time + datetime.timedelta(hours=2)
        cursor.execute("INSERT INTO ADMIN_SESSION VALUES (?, ?, ?, ?)",
                       (session_id, username, login_time, expire_time))
        db_connection.commit()
        db_connection.close()
        return session_id

    db_connection.close()
    return None


def admin_register_db(username, password):
    db_connection = sqlite3.connect('localServer.db')
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO ADMINS VALUES (?, ?)",
                   (username, hashlib.md5(password.encode()).hexdigest()))
    db_connection.commit()
    db_connection.close()


def admin_user_register_db(username, password):
    db_connection = sqlite3.connect('localServer.db')
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO ADMINS VALUES (?, ?)",
                   (username, hashlib.md5(password.encode()).hexdigest()))
    db_connection.commit()
    db_connection.close()


### Routes ###

@server.route("/api/admin/login", methods=["POST"])
def admin_login():
    body_data = request.get_json()
    try:
        username = body_data["username"]
        password = body_data["password"]
        if(username.strip() and password.strip()):
            session_id = admin_login_db(username, password)
            if session_id is not None:
                return json.dumps({"status": "success", "sessionId": session_id})
            else:
                return json.dumps({"status": "error", "reason": "invalid user pass"})
        else:
            return json.dumps({"status": "error", "reason": "empty"})
    except Exception as e:
        return json.dumps({"status": "error", "reason": e.__class__.__name__})


@server.route("/api/admin/register", methods=["POST"])
def admin_register():
    body_data = request.get_json()
    try:
        username = body_data["username"]
        password = body_data["password"]
        if(username.strip() and password.strip()):
            admin_register_db(username, password)
            return json.dumps({"status": "success"})
        else:
            return json.dumps({"status": "error", "reason": "empty"})
    except Exception as e:
        return json.dumps({"status": "error", "reason": e.__class__.__name__})


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
