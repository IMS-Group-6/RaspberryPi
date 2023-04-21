import socketio
import json
import asyncio
import aiohttp


class SocketIOClient:
    def __init__(self, server_url, connector):
        self.connector = connector
        connector = aiohttp.TCPConnector(ssl=False)
        http_session = aiohttp.ClientSession(connector=connector)

        self.sio = socketio.AsyncClient(
            reconnection=True,
            reconnection_delay=5,
            http_session=http_session
        )
        self.server_url = server_url

        # Event Listeners
        self.sio.on('connect', self.on_connect_or_reconnect)
        # I think this is an event, not sure xd
        self.sio.on('reconnect', self.on_connect_or_reconnect)
        self.sio.on('message', self.on_message)

    async def connect(self):
        await self.sio.connect(self.server_url)

    async def emit(self, data):
        await self.sio.emit('message', json.dumps(data))

    async def _register_as_mower(self):
        data = {
            "type": "MOWER_REGISTRATION",
            "data": {
                "role": "mower"
            }
        }
        await self.emit(data)

    async def on_connect_or_reconnect(self):
        await self._register_as_mower()

    async def on_message(self, raw_data):
        """
        This function handles all types of events.
        At the moment these are the events that can be received:

        - DRIVING_MODE (manual or auto)
            - example:
                {
                    "type": "DRIVING_MODE",
                    "data": {
                        "mode": "auto"
                    }
                }

        - MOWER_COMMAND (forward, backward, left or right)
            - example:
                {
                    "type": "MOWER_COMMAND",
                    "data": {
                        "direction": "left"
                    }
                }
        """
        try:
            data = json.loads(raw_data)
            print(data)

            if data['type'] == 'DRIVING_MODE':
                mode = data['data']['mode']
                print(f"Driving mode: {mode}")

            elif data['type'] == 'MOWER_COMMAND':
                direction = data['data']['direction']
                print(f"Received direction: {direction}")

                if direction == 'forward':
                    self.connector.forward()
                elif direction == 'backward':
                    self.connector.backward()
                elif direction == 'left':
                    self.connector.left()
                elif direction == 'right':
                    self.connector.right()
        except Exception as e:
            print('Error: ', e)

    # We can send mower position every second or so through socket or rest api
    # (and requirements), up to you to decide. Maybe ask the supervisor next week?
    async def send_mower_position(self, mowing_session_id, x, y):
        data = {
            "type": "MOWER_POSITION",
            "data": {
                "sessionId": mowing_session_id,
                "x": x,
                "y": y
            }
        }
        await self.emit(data)


async def main():
    client = SocketIOClient('http://localhost:8080')
    await client.connect()

    await client.send_mower_position("abc123", 10, 20)

    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())
