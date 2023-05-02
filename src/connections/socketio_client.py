import socketio
import json
import aiohttp
import config

class SocketIOClient:
    def __init__(self):
        tcp_connector = aiohttp.TCPConnector(ssl=False)
        http_session = aiohttp.ClientSession(connector=tcp_connector)

        self.sio = socketio.AsyncClient(
            reconnection=True,
            reconnection_delay=5,
            http_session=http_session
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
        await self.sio.connect(self.server_url)

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
