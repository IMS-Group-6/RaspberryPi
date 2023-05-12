# Library imports
import time
import logging
import asyncio
import json
from websocket_client import WebSocketClient
# from module.Camera import Camera

# File imports
from connector import Connector
from odometry import Odemetry


def main():
    con = Connector()
    odom = Odemetry()

    websocket_client = WebSocketClient(con)
    websocket_client.start()

    # camera = Camera()

    if con.connected:
        try:
            while True:
                data = con.read_data()

                match data:
                    case "CAPTURE":
                        print('Object detected! Capturing Image...')
                        # camera.capture("test-image.jpg")
                    case "ENCODER":
                        odom.solve(con.l, con.r)
                    case "BORDER":
                        odom.border()
                    case _:
                        pass

        except KeyboardInterrupt:
            logging.info("Keyboard interrupt received, stopping...")
            # Gracefully stop the motors on KeyboardInterrupt
            con.stop()
            con.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()

