import logging
import asyncio
import threading

# File imports
from module.Camera import Camera
from connections.api_client import APIClient
from connections.connector import Connector
from command_handler import CommandHandler

def main():
    con = Connector()
    camera = Camera()
    api_client = APIClient()

    if con.connected:
        while True:
            # Should boundary and obstacle events be sent from here?
            data = con.read_data()

            if data == "CAPTURE":
                print('Object detected! Capturing Image...')
                # This is the function which will capture an image and store it to the local folder if nothing else is entered
                camera.capture("test-image.jpg")


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
