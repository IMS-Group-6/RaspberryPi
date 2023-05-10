# Library imports
import logging
import asyncio
import threading

# File imports
from module.Camera import Camera
from connections.api_client import APIClient
from connections.connector import Connector
from command_handler import CommandHandler

from connector import Connector # You should remove this file and modify connections.connector and connections.base.connector
from odometry import Odemetry

def main():
    global api_client, con
    
    odom = Odemetry()
    camera = Camera()

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

    api_client = APIClient()
    con = Connector()
    command_handler = CommandHandler(api_client=api_client, connector=con)

    # Start the main() function in a separate thread
    t = threading.Thread(target=main, daemon=True)
    t.start()

    try:
        asyncio.run(command_handler.listen())
    except asyncio.exceptions.CancelledError:
        logging.info("Keyboard interrupt received, stopping...")
        if (con.connected):
            
            # Stops an active session before program termination
            api_response = api_client.stop_mowing_session()

            if api_response.success:
                print(f"Stopped an active session before program termination, status code: {api_response.status_code}")
            elif not api_response.success and api_response.status_code == 400:
                print(f"No active session was found before program termination, status code: {api_response.status_code}")
            else:
                print(f"Failed to stop session, status code: {api_response.status_code}")
            
            con.stop()
            con.close()
