from connections.socketio_client import SocketIOClient 
from connections.connector import Connector
import asyncio
import json
import logging

class CommandHandler:
    def __init__(self):
        self.sio_client = SocketIOClient("http://localhost:8080")
        self.connector = Connector()

        self.auto_mode = True

    async def listen(self):
        """
        Connects to the Socket.IO server and starts listening to incoming commands.

        Args:
        - None

        Returns:
        - None
        """
        await self.sio_client.connect()
        self.sio_client.sio.on('message', self._handle_message)
        await self.sio_client.sio.wait()
        # or self.sio_client.sio.sleep() to not block main thread. But it will probably be used differently
    
    def _handle_message(self, raw_data):
        """
        Parses a raw message received from the server and passes the resulting data to the process_message() function.

        Args:
        - raw_data: A string representing the raw message received from the server.

        Returns:
        - None
        """
        try:
            parsed_data = json.loads(raw_data)
            self._process_message(parsed_data)
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse message: {raw_data}")
            return None
        except Exception as e:
            logging.error(e)
            return None
    
    def _process_message(self, data):
        """
        Processes a parsed message received from the server.

        Args:
        - data: A dictionary representing the parsed data received from the server.

        Returns:
        - None
        """
        event_type = data.get("type")
        event_data = data.get("data")

        if event_type == "DRIVING_MODE":
            self._proccess_driving_mode_event(event_data)
        elif event_data == "MOWER_COMMAND":
            self._proccess_mower_command_event(event_data)
        else:
            logging.info(f"Unrecognized event type: {event_type}")
    
    def _proccess_driving_mode_event(self, event_data):
        """
        Processes the "DRIVING_MODE" event received from the server and updates the 'self.auto_mode' attribute accordingly.

        Args:
        - event_data: A dictionary representing the data received in the "DRIVING_MODE" event.

        Returns:
        - None
        """
        driving_mode = event_data.get("mode")

        if driving_mode == "auto":
            if self.auto_mode:
                return
            
            self.auto_mode = True
            self.connector.drive_autonomously()

        elif driving_mode == "manual":
            if not self.auto_mode:
                return

            self.auto_mode = False
            # Couldnt find a command for manual mode
        else:
            logging.info(f"Unrecognized driving mode: {event_data}")

    def _proccess_mower_command_event(self, event_data):
        """
        Processes the "MOWER_COMMAND" event received from the server.

        Args:
        - event_data: A dictionary representing the data received in the "MOWER_COMMAND" event.

        Returns:
        - None
        """
        direction = event_data.get("direction")
        
        if direction == "forward":
            self.connector.forward()
        elif direction == "backward":
            self.connector.backward()
        elif direction == "left":
            self.connector.left()
        elif direction == "right":
            self.connector.right()
        else:
            logging.info(f"Unrecognized direction: {event_data}")

# This code should be in main or something
async def main():
    a = CommandHandler()
    await a.listen()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
