# python3.6

import json
import random
import requests
from paho.mqtt import client as mqtt_client

from CustomError import CustomError

broker = 'localhost'
port = 1883
topic_board_send = "python/board/send"
topic_board_receive = "python/board/receive"
client_id = f'server-{random.randint(0, 100)}'

LOCAL_SERVER_API_URL = "http://localhost:5000"
DEFAULT_REQUEST_HEADER = {"Content-Type": "application/json"}


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        message_body = msg.payload.decode()
        print(f"Received `{message_body}` from `{msg.topic}` topic")
        cmd = message_body.split(",")
        if cmd[0] == "login":
            server_request_payload = {
                "user_id": cmd[1].strip(),
                "password": cmd[2].strip(),
                "light": cmd[3].strip()
            }

            main_server_json_result = requests.post(LOCAL_SERVER_API_URL+"/api/user/login",
                                                    data=json.dumps(server_request_payload), headers=DEFAULT_REQUEST_HEADER).json()

            client.publish(topic_board_receive,
                           json.dumps(main_server_json_result))
        elif cmd[0] == "exit":
            client.disconnect()
            client.loop_stop()
            print("Disconnected from MQTT Broker")
    client.subscribe(topic_board_send)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
