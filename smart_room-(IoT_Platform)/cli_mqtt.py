# python 3.6

import random
from paho.mqtt import client as mqtt_client


broker = 'localhost'
port = 1883
topic_board_send = "python/board/send"
topic_board_receive = "python/board/receive"
client_id = f'client-{random.randint(0, 1000)}'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    while True:
        cmd = input("Enter command or type 'exit': ")
        cmds = cmd.split()
        if cmds[0] == 'exit':
            payload = f'exit'
            result = client.publish(topic_board_send, payload)
            if result[0] == 0:
                print(f"Exit command sent to MQTT Broker")
            else:
                print(f"Failed to send exit to Local Server")
            break
        elif cmds[0] == 'login':
            user_id = cmds[1]
            password = cmds[2]
            payload = f'login,{user_id},{password},{random.randint(0, 100)}'
            result = client.publish(topic_board_send, payload)
            status = result[0]
            if status == 0:
                print(f"Command Sent to Local Server Successfully")
            else:
                print(f"Failed to send Message to Local Server")


def subscribe_to_reponse(client: mqtt_client):
    def on_message_receive(client, userdata, msg):
        message_body = msg.payload.decode()
        print(f"Local Server Response `{message_body}`")

    client.subscribe(topic_board_receive)
    client.on_message = on_message_receive


def run_mqtt():
    client = connect_mqtt()
    client.loop_start()
    subscribe_to_reponse(client)
    publish(client)


if __name__ == '__main__':
    run_mqtt()
