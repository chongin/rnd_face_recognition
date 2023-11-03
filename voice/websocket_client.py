import asyncio
import websockets
import json


class WebSocketClient:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None

    async def connect(self):
        self.websocket = await websockets.connect(self.uri)
        if not self.websocket:
            raise Exception(f"Connect to this server: {self.uri} failed.")

    async def receive_message(self):
        while True:
            response = await self.websocket.recv()
            await self.handle_server_message(response)

    async def handle_server_message(self, message):
        json_msg = json.loads(message)
        print(f"Received message from server: {json_msg}")
       
    async def send_message(self, message: dict):
        if type(message) is dict:
            message = json.dumps(message)

        await self.websocket.send(message)
        print(f"Sent message to server: {message}")


# async def run(cliient):
#     await client.connect()
#     await asyncio.gather(
#         client.receive_message()
#     )

# if __name__ == "__main__":
#     client = WebSocketClient("ws://localhost:8765")

