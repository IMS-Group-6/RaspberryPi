import time
import logging
import asyncio
import json


# File imports
import Connector
from connections.socket_client import SocketIOClient
from module.Camera import Camera


# Main program
async def main():
    con = Connector.Connector()
    message_queue = asyncio.Queue()
    websocket_client = SocketIOClient(
        'http://localhost:3000', message_queue)  # Test server URL

   # websocket_client = SocketIOClient('http://localhost:8080', con)  # Real server

    await websocket_client.emit({"type": "TEST_MESSAGE", "data": "Hello, server"})

    camera = Camera()

    if con.connected:
        try:
            while True:
                try:
                    raw_data = await asyncio.wait_for(message_queue.get(), timeout=5)
                    print(f"Message retrieved from queue: {raw_data}")
                except asyncio.TimeoutError:
                    print("No messages received for 5 seconds")
                data = json.loads(raw_data)
                print(data)
                try:
                    if data['type'] == 'DRIVING_MODE':
                        mode = data['data']['mode']
                        print(f"Driving mode: {mode}")

                    elif data['type'] == 'MOWER_COMMAND':
                        direction = data['data']['direction']
                        print(f"Received direction: {direction}")

                        if direction == 'forward':
                            con.forward()
                            asyncio.sleep(100)
                        elif direction == 'backward':
                            con.backward()
                        elif direction == 'left':
                            print('Turn left')
                            con.left()
                        elif direction == 'right':
                            con.right()
                except Exception as e:
                    print('Error: ', e)

        except KeyboardInterrupt:
            logging.info("Keyboard interrupt received, stopping...")
            # Gracefully stop the motors on KeyboardInterrupt
            con.stop()
            con.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())

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
