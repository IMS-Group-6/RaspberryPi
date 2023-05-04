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
        try:
            while True:
                # Should boundary and obstacle events be sent from here?
                data = con.read_data()

                if data == "CAPTURE":
                    print('Object detected! Capturing Image...')
                    # This is the function which will capture an image and store it to the local folder if nothing else is entered
                    camera.capture("test-image.jpg")

        except KeyboardInterrupt:
            logging.info("Keyboard interrupt received, stopping...")
            # Gracefully stop the motors on KeyboardInterrupt
            con.stop()
            con.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    t = threading.Thread(target=main)
    t.start()
    
    command_handler = CommandHandler()
    asyncio.run(command_handler.listen())
