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


@server.route("/api/user/<usr>", methods=["GET"])
def user_setting(usr):
    lights_value = request.args.get("lights")
    return "<h1>Hello, " + usr + ", " + lights_value + "</h1>"


if __name__ == '__main__':
    server.run(debug=True, port=5001)
