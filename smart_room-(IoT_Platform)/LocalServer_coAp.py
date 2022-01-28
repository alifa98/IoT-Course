import asyncio
import json

import aiocoap.resource as resource
import aiocoap
import requests
LOCAL_SERVER_API_URL = "http://localhost:5000"
DEFAULT_REQUEST_HEADER = {"Content-Type": "application/json"}


class MyResource(resource.Resource):

    def __init__(self):
        super().__init__()

    async def render_put(self, request):
        message_body = request.payload.decode('utf-8')
        cmd = message_body.split(",")
        if cmd[0] == "login":
            server_request_payload = {
                "user_id": cmd[1].strip(),
                "password": cmd[2].strip(),
                "light": cmd[3].strip()
            }

            main_server_json_result = requests.post(LOCAL_SERVER_API_URL+"/api/user/login",
                                                    data=json.dumps(server_request_payload), headers=DEFAULT_REQUEST_HEADER).json()

            return aiocoap.Message(payload=json.dumps(main_server_json_result).encode('utf-8'))


async def main():

    # Resource tree creation
    root = resource.Site()
    root.add_resource(['request'], MyResource())

    await aiocoap.Context.create_server_context(root)

    # Run forever
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())
