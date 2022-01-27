import datetime
import hashlib
import sqlite3
from flask import *

from markupsafe import re
from CustomError import CustomError

from Utils import catch_all_exceptions, check_empty_error, create_response

server = Flask(__name__)

LOCAL_SQLITE_DB_PATH = "mainServer.db"
DEFAULT_LIGHT_VALUE = 50
SERVER_API_KEY = "9634024"


## DATABASE ##


def user_register_db(password, office, room):
    db_connection = sqlite3.connect(LOCAL_SQLITE_DB_PATH)
    cursor = db_connection.cursor()
    cursor.execute(
        "INSERT INTO `USERS` (`PASSWORD`, `LIGHT`, `OFFICE`, `ROOM`) VALUES (?, ?, ?, ?) ;",
        (hashlib.md5(password.encode()).hexdigest(),
         DEFAULT_LIGHT_VALUE, office, int(room))
    )
    user_id = cursor.lastrowid
    db_connection.commit()
    db_connection.close()

    return user_id


def get_office_activity_db(office):
    db_connection = sqlite3.connect(LOCAL_SQLITE_DB_PATH)
    cursor = db_connection.cursor()
    query = cursor.execute(
        "SELECT * FROM `ACTIVITY` WHERE `OFFICE` = ? ;",
        (office,)
    )
    columns_name = [str(c[0]).lower() for c in query.description]
    activity_rows = [dict(zip(columns_name, row)) for row in query.fetchall()]
    db_connection.close()

    return activity_rows


def check_user_and_log_activity_and_get_light_db(user_id, office):
    db_connection = sqlite3.connect(LOCAL_SQLITE_DB_PATH)
    cursor = db_connection.cursor()

    cursor.execute(
        "SELECT `LIGHT` FROM `USERS` WHERE `ID` = ? and `OFFICE` = ? ;",
        (user_id, office)
    )

    user_row = cursor.fetchone()

    if user_row is not None:
        cursor.execute(
            "INSERT INTO ACTIVITY VALUES (?, ?, ?, ?);",
            (user_id, office, datetime.datetime.now(), "LOGIN")
        )
        db_connection.commit()
        db_connection.close()
        return user_row[0]  # light value

    db_connection.close()
    raise CustomError("Error in Activity Logging")


## Utiles ##


def check_server_api_key(json_body):
    try:
        if SERVER_API_KEY != json_body["apiKey"]:
            raise CustomError("Invalid API Key")
    except CustomError as e:
        raise e
    except Exception:
        raise CustomError("Error in server's api key checking")


## ROUTES ##


@server.route("/api/user/register", methods=["POST"])
@catch_all_exceptions
def user_register():
    body_data = request.get_json()
    check_server_api_key(body_data)

    password = check_empty_error(body_data["password"])
    office = check_empty_error(body_data["office"])
    room = check_empty_error(body_data["room"])

    user_id = user_register_db(password, office, room)

    return create_response(True, {"user_id": user_id})


@server.route("/api/user/activities", methods=["POST"])
@catch_all_exceptions
def get_user_office_activities():
    body_data = request.get_json()
    check_server_api_key(body_data)

    office = check_empty_error(body_data["office"])

    office_activity_list = get_office_activity_db(office)

    return create_response(True, {"activities": office_activity_list})


@server.route("/api/user/login", methods=["POST"])
@catch_all_exceptions
def user_login():
    body_data = request.get_json()
    check_server_api_key(body_data)

    user_id = check_empty_error(body_data["user_id"])
    office = check_empty_error(body_data["office"])

    # this line checks that user is in the database and ensure that it belongs to the office.
    light = check_user_and_log_activity_and_get_light_db(user_id, office)

    return create_response(True, {"light": light})


if __name__ == '__main__':
    server.run(debug=True, port=5001)
