import logging
import asyncio
import random

from aiocoap import *


async def main():
    protocol = await Context.create_client_context()
    while True:
        request_payload = None
        cmd = input("Enter command or type 'exit': ")
        cmds = cmd.split()
        if cmds[0] == 'exit':
            request_payload = 'exit'
        elif cmds[0] == 'login':
            user_id = cmds[1]
            password = cmds[2]
            request_payload = f'login,{user_id},{password},{random.randint(0, 100)}'

        request = Message(code=PUT, payload=request_payload.encode('utf-8'),
                          uri="coap://localhost/request")

        try:
            response = await protocol.request(request).response
            print(f"Command Sent to Local Server Successfully")
        except Exception as e:
            print('Failed to fetch resource:')
            print(e)
        else:
            print(f'response: {response.payload.decode("utf-8")}')

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError:
        pass
