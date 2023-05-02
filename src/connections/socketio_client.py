import socketio
import json
import aiohttp

class SocketIOClient:
    def __init__(self, server_url):
        tcp_connector = aiohttp.TCPConnector(ssl=False)
        http_session = aiohttp.ClientSession(connector=tcp_connector)

        self.sio = socketio.AsyncClient(
            reconnection=True,
            reconnection_delay=5,
            http_session=http_session
        )
        self.server_url = server_url

        # Event Listeners
        self.sio.on('connect', self._register_as_mower)
        self.sio.on('reconnect', self._register_as_mower)
        self.sio.on('message', self.on_message)

    async def connect(self):
        """
        Connects to the Socket.IO server.

        Args:
        - None

        Returns:
        - None
        """
        await self.sio.connect(self.server_url)

    async def _emit(self, data):
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
        await self._emit(data)

    async def on_message(self, raw_data):
        """
        Event listener that is triggered when a "message" event is received from the Socket.IO server.

        Args:
        - raw_data: A string representing the raw data received from the server.

        Returns:
        - The parsed JSON data received from the server.
        """
        print(f"Received message: {raw_data}")
        try:
            data = json.loads(raw_data)
            return data
        except Exception as e:
            print("Error: ", e)
