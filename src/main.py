# Library imports
import time
import logging
import asyncio
import json
import threading
from websocket_client import WebSocketClient
from module.Camera import Camera
from connections.api_client import APIClient
from connections.connector import Connector
from command_handler import CommandHandler

# File imports
from connector import Connector
from odometry import Odemetry


def main():
    con = Connector()
    odom = Odemetry()
    camera = Camera()
    api_client = APIClient()

    if con.connected:
        while True:
            # Should boundary and obstacle events be sent from here?
            data = con.read_data()

                match data:
                    case "CAPTURE":
                        print('Object detected! Capturing Image...')
                        camera.capture("test-image.jpg")
                    case "ENCODER":
                        odom.solve(con.l, con.r)
                    case _:
                        pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    t = threading.Thread(target=main, daemon=True)
    t.start()

    api_client = APIClient() # Singleton
    con = Connector() # Singleton
    command_handler = CommandHandler(connector=con)
    
    try:
        asyncio.run(command_handler.listen())
    except asyncio.exceptions.CancelledError:
        logging.info("Keyboard interrupt received, stopping...")
        if (con.connected):
            print("\n----")

            # Stops an active session before program termination
            if api_client.stop_mowing_session():
                print("Stopped an active session before program termination")
            else:
                print("No active session was found before program termination")
            
            con.stop()
            con.close()
