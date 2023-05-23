import socketio
import json
import aiohttp
import config
import asyncio


class SocketIOClient:
    def __init__(self):
        """
        This is a constructor function that initializes a socketio client with event listeners for
        'connect' and 'reconnect'.
        """
        self.sio = socketio.AsyncClient(
            reconnection=True,
            reconnection_delay=5
        )
        self.server_url = config.SERVER_URL

        # Event Listeners
        # "message" event is handled in the command file
        self.sio.on('connect', self._register_as_mower)
        self.sio.on('reconnect', self._register_as_mower)

    async def connect(self):
        """
        Connects to the Socket.IO server.

        Args:
        - None

        Returns:
        - None
        """
        async def create_session_and_connect():
            tcp_connector = aiohttp.TCPConnector(ssl=False)
            async with aiohttp.ClientSession(connector=tcp_connector) as session:
                self.sio.http_session = session
                await self.sio.connect(self.server_url)

        await asyncio.create_task(create_session_and_connect())

    async def emit(self, data):
        """
        Emits a Socket.IO event with the specified data.

        Args:
        - data: A dictionary representing the data to be sent in the event.

        Returns:
        - None
        """
        await self.sio.emit('message', json.dumps(data))

    async def _register_as_mower(self):
        """
        Sends a "MOWER_REGISTRATION" event to the Socket.IO server to register as a mower.

        Args:
        - None

        Returns:
        - None
        """
        data = {
            "type": "MOWER_REGISTRATION",
            "data": {
                "role": "mower"
            }
        }
        await self.emit(data)
