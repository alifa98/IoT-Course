import datetime
from functools import wraps
import hashlib
import secrets
import string
from flask import *
import sqlite3
import requests

from CustomError import CustomError
from Utils import catch_all_exceptions, check_empty_error, create_response

server = Flask(__name__)

LOCAL_SQLITE_DB_PATH = "localServer.db"
LOCAL_OFFICE_ID = 1
MAIN_SERVER_API_URL = "http://localhost:5001"
MAIN_SERVER_API_KEY = "9634024"
DEFAULT_REQUEST_HEAAADER = {"Content-Type": "application/json"}

### Database ###


def admin_login_db(username, password):
    db_connection = sqlite3.connect(LOCAL_SQLITE_DB_PATH)
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
    db_connection = sqlite3.connect(LOCAL_SQLITE_DB_PATH)
    cursor = db_connection.cursor()
    # We did not consider `EXPIRE_DATE` because the assignment had not mentioned it, but if we wanted to consider, we could add `AND s.EXPIRE_DATE > now()` to the WHERE clause in the following query (notice: the sqlite does not have now() function like mysql, so it should be replaced with something that works in Sqlite)
    cursor.execute(
        "SELECT * FROM ADMIN_SESSION s WHERE s.ID = ? ;", (session_id,)
    )
    return cursor.fetchone() is not None


def admin_register_db(username, password):
    db_connection = sqlite3.connect(LOCAL_SQLITE_DB_PATH)
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO ADMINS VALUES (?, ?)",
                   (username, hashlib.md5(password.encode()).hexdigest()))
    db_connection.commit()
    db_connection.close()


def admin_user_register_db(user_id, password, room):
    db_connection = sqlite3.connect(LOCAL_SQLITE_DB_PATH)
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO USERS VALUES (?, ?, ?)",
                   (int(user_id), hashlib.md5(password.encode()).hexdigest(), int(room)))
    db_connection.commit()
    db_connection.close()


### Utilities ###
def check_admin_session(json_body):
    try:
        session_id = check_empty_error(json_body["sessionId"])
        if(not check_admin_auth_db(session_id)):
            raise CustomError("Invalid Token")
    except Exception:
        raise CustomError("Error in admin's session checking")


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
@catch_all_exceptions
def admin_user_register():
    body_data = request.get_json()
    check_admin_session(body_data)

    password = check_empty_error(body_data["password"])
    room = check_empty_error(body_data["room"])
    main_server_request_payload = {
        "apiKey": MAIN_SERVER_API_KEY,
        "password": password,
        "office": LOCAL_OFFICE_ID,
        "room": room
    }
    main_server_json_result = requests.post(MAIN_SERVER_API_URL+"/api/user/register",
                                            data=json.dumps(main_server_request_payload), headers=DEFAULT_REQUEST_HEAAADER).json()
    if(main_server_json_result["status"] != "success"):
        raise CustomError(main_server_json_result["reason"])

    user_id = main_server_json_result["user_id"]

    admin_user_register_db(user_id, password, room)

    return create_response(True, {"user_id": user_id})


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
