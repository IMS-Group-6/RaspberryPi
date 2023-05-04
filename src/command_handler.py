from connections.socketio_client import SocketIOClient
from connections.api_client import APIClient
from enum import Enum
import json
import logging

class DrivingMode(Enum):
    AUTO = 1
    MANUAL = 2

class RunState(Enum):
    START = 1
    STOP = 2

class CommandHandler:
    def __init__(self, connector):
        self.sio_client = SocketIOClient()
        self.api_client = APIClient()
        self.connector = connector

        # Keep track of different operations
        self.driving_mode = DrivingMode.AUTO
        self.run_state = RunState.STOP

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
        print(raw_data)
        try:
            parsed_data = json.loads(raw_data)
            self._process_message(parsed_data)
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse message: {raw_data}")
        except Exception as e:
            logging.error(e)

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
        elif event_type == "MOWER_COMMAND":
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
            if self.driving_mode == DrivingMode.AUTO:
                logging.debug("Driving mode is already AUTO")
                return
            
            self.driving_mode = DrivingMode.AUTO
            self.connector.drive_autonomously()

        elif driving_mode == "manual":
            if self.driving_mode == DrivingMode.MANUAL:
                logging.debug("Driving mode is already MANUAL")
                return
            
            self.driving_mode = DrivingMode.MANUAL
            self.connector.manual()
        else:
            logging.info(f"Unrecognized driving mode: {driving_mode}")

    def _proccess_mower_command_event(self, event_data):
        """
        Processes the "MOWER_COMMAND" event received from the server.

        Args:
        - event_data: A dictionary representing the data received in the "MOWER_COMMAND" event.

        Returns:
        - None
        """
        action = event_data.get("action")

        if (action in ("forward", "backward", "left", "right") and 
            (self.run_state != RunState.START or self.driving_mode != DrivingMode.MANUAL)):
                logging.debug("Mower must be in START state and in MANUAL driving mode")
                return
        
        if action == "forward":
            self.connector.forward()
        elif action == "backward":
            self.connector.backward()
        elif action == "left":
            self.connector.left()
        elif action == "right":
            self.connector.right()
        elif action == "start":
            self._start_action()
        elif action == "stop":
            self._stop_action()
        else:
            logging.debug(f"Unrecognized action: {action}")

    def _start_action(self):
        """
        Handles a "start" event received from the server.

        Args:
        - None

        Returns:
        - None
        """
        if self.run_state == RunState.START:
            logging.debug("Run state is already START")
            return

        if self.api_client.start_mowing_session():
            self.run_state = RunState.START
            self.connector.start()
        else:
            logging.error("Failed to start a mowing session")

    def _stop_action(self):
        """
        Handles a "stop" event received from the server.

        Args:
        - None

        Returns:
        - None
        """
        if self.run_state == RunState.STOP:
            logging.debug("Run state is already STOP")
            return

        if self.api_client.stop_mowing_session():
            self.run_state = RunState.STOP
            self.driving_mode = DrivingMode.AUTO
            self.connector.stop()
        else:
            logging.error("Failed to stop a mowing session")
