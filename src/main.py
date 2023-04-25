import time
import logging
import asyncio
import json


# File imports
import Connector
from websocket_client import WebSocketClient
#from module.Camera import Camera


def main():
    con = Connector.Connector()

    websocket_client = WebSocketClient(con)
    websocket_client.start()

   # camera = Camera()

    if con.connected:
        try:
            while True:
                data = con.read_data()

                if data == "CAPTURE":
                    print('Object detected! Capturing Image...')
                    #camera.capture("test-image.jpg")

        except KeyboardInterrupt:
            logging.info("Keyboard interrupt received, stopping...")
            # Gracefully stop the motors on KeyboardInterrupt
            con.stop()
            con.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())

