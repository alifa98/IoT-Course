from flask import *

from markupsafe import re

server = Flask(__name__)


@server.route("/api/user/<usr>", methods=["GET"])
def user_setting(usr):
    lights_value = request.args.get("lights")
    return "<h1>Hello, " + usr + ", " + lights_value + "</h1>"


if __name__ == '__main__':
    server.run(debug=True, port=5001)
